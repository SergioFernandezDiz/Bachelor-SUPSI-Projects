"""
Frankie Pick-and-Place Simulation
Simulates Frankie robot executing a pick-and-place task with a lightbulb.
"""

from __future__ import annotations

from typing import Optional, Sequence, Tuple
import time
import numpy as np
import roboticstoolbox as rtb
import spatialgeometry as sg
import spatialmath as sm
import swift
import matplotlib as mtb
import matplotlib.pyplot as plt

mtb.rcParams.update(mtb.rcParamsDefault)

# Import controller
from frankie_controller import FrankieController, FrankieControllerParams, TaskState

# Visual parameters
COLOR_RED = (0.8, 0.2, 0.3, 1.0)
COLOR_BLUE = (0.2, 0.5, 0.8, 1.0)
COLOR_GREEN = (0.2, 0.8, 0.3, 1.0)
COLOR_YELLOW = (0.9, 0.8, 0.2, 1.0)
COLOR_WHITE = (1.0, 1.0, 1.0, 0.6)
COLOR_GRAY = (0.5, 0.5, 0.5, 1.0)

BULB_RADIUS = 0.03
FIXTURE_RADIUS = 0.02
FLOOR_HEIGHT = 0.02


class FrankieAgent:
    """Bundle Frankie robot model and Swift visualization."""

    def __init__(self, name: str, start_config: Sequence[float], start_base_pose: Tuple[float, float, float]) -> None:
        self.name = name
        # Use URDF Frankie model (has proper joint limits for Swift)
        self._robot = rtb.models.URDF.Frankie()
        self._robot.q = np.array(start_config, dtype=float)
        
        # Set base pose (mobile base position)
        self._base_pose = np.array(start_base_pose, dtype=float)  # [x, y, theta]
        self._update_base_transform()

    def _update_base_transform(self) -> None:
        """Update robot base transform based on mobile base pose."""
        x, y, theta = self._base_pose
        # Set base transform (mobile base position)
        self._robot.base = sm.SE3(x, y, 0.0) * sm.SE3.Rz(theta)

    def register(self, env: swift.Swift) -> None:
        env.add(self._robot)

    def q(self) -> np.ndarray:
        return np.asarray(self._robot.q, dtype=float)

    def base_state(self) -> np.ndarray:
        """Get mobile base state [x, y, theta]."""
        return self._base_pose.copy()

    def apply_velocity_cmd(self, qdot: np.ndarray, base_cmd: Optional[Tuple[float, float]] = None) -> None:
        """Apply joint velocities and update mobile base if needed."""
        dt = 0.05  # Should match simulation dt
        
        if base_cmd is not None:
            # Use unicycle dynamics for base pose tracking
            v, omega = base_cmd
            self._base_pose[0] += v * np.cos(self._base_pose[2]) * dt
            self._base_pose[1] += v * np.sin(self._base_pose[2]) * dt
            self._base_pose[2] += omega * dt
            # Wrap angle
            self._base_pose[2] = (self._base_pose[2] + np.pi) % (2 * np.pi) - np.pi
            self._update_base_transform()
            # Don't apply base joint velocities - base is controlled via transform
            # Only apply arm joint velocities
            qdot_arm = qdot.copy()
            qdot_arm[0] = 0.0  # Don't move base rotation joint
            qdot_arm[1] = 0.0  # Don't move base translation joint
            self._robot.qd = qdot_arm
        else:
            # No base command - update base from joint velocities if they're non-zero
            omega = qdot[0] if len(qdot) > 0 else 0.0
            v = qdot[1] if len(qdot) > 1 else 0.0
            if abs(omega) > 1e-6 or abs(v) > 1e-6:
                # Convert base joint velocities to unicycle motion
                # Joint 1 translates along base x-axis, need to project to world
                self._base_pose[0] += v * np.cos(self._base_pose[2]) * dt
                self._base_pose[1] += v * np.sin(self._base_pose[2]) * dt
                self._base_pose[2] += omega * dt
                self._base_pose[2] = (self._base_pose[2] + np.pi) % (2 * np.pi) - np.pi
                self._update_base_transform()
            # Apply all joint velocities
            self._robot.qd = qdot


def add_world_bounds(env: swift.Swift, bounds: Tuple[float, float, float, float]) -> sg.Cuboid:
    """Draw a translucent floor tile highlighting the workspace."""
    min_x, max_x, min_y, max_y = bounds
    width, depth = max_x - min_x, max_y - min_y
    floor = sg.Cuboid(scale=[width, depth, FLOOR_HEIGHT], color=COLOR_WHITE)
    floor.T = sm.SE3((min_x + max_x) / 2.0, (min_y + max_y) / 2.0, 0.01)
    env.add(floor)
    return floor


def add_wall(env: swift.Swift, position: Tuple[float, float, float], size: Tuple[float, float, float]) -> sg.Cuboid:
    """Add a wall to the environment."""
    wall = sg.Cuboid(scale=size, color=COLOR_GRAY)
    wall.T = sm.SE3(*position)
    env.add(wall)
    return wall


def main() -> None:
    # Simulation parameters
    dt = 0.05
    simulation_time = 90.0  # seconds (increased for larger environment)
    
    # Much larger environment for Frankie robot
    world_bounds = (-4.0, 4.0, -4.0, 4.0)  # min_x, max_x, min_y, max_y (8m x 8m workspace)
    min_x, max_x, min_y, max_y = world_bounds

    # Launch Swift viewer
    env = swift.Swift()
    env.launch(realtime=True, comms="rtc", browser="browser")
    time.sleep(1.0)

    # Create workspace floor
    add_world_bounds(env, world_bounds)

    # Create wall with fixture (positioned on one side of the larger environment)
    wall_position = (3.5, 0.0, 0.5)  # x, y, z (center of wall) - moved further
    wall_size = (0.1, 2.0, 1.2)  # thickness, width, height - wider and taller wall
    wall = add_wall(env, wall_position, wall_size)
    
    # Wall fixture / target position (where bulb will be screwed) - higher on wall
    # Place it slightly in front of the wall surface so it's visible and reachable
    screw_x = wall_position[0] - wall_size[0] / 2.0 - 0.02
    fixture_position = (screw_x, 0.0, 0.8)  # target point for control and visualization
    fixture_visual = sg.Sphere(
        radius=FIXTURE_RADIUS * 2.0,   # make marker larger and clearly visible
        pose=sm.SE3(*fixture_position),
        color=COLOR_RED,               # bright red marker on the wall
    )
    env.add(fixture_visual)

    # Spawn lightbulb at random location on top of a square tower,
    # ensuring it's not too close to robot base
    rng = np.random.default_rng()
    robot_base_pos = (0.0, 0.0)  # Robot starts at origin
    min_distance_from_base = 1.0  # Minimum distance from robot base (meters)
    max_attempts = 100
    
    tower_height = 0.40  # meters
    bulb_z = tower_height + 0.05  # bulb slightly above top surface
    bulb_position = None
    
    for attempt in range(max_attempts):
        bulb_x = float(rng.uniform(min_x + 0.5, max_x - 1.0))  # Keep away from edges
        bulb_y = float(rng.uniform(min_y + 0.5, max_y - 0.5))
        
        # Check distance from robot base
        dist_from_base = np.hypot(bulb_x - robot_base_pos[0], bulb_y - robot_base_pos[1])
        
        # Also ensure it's not too close to the wall
        dist_from_wall = abs(bulb_x - wall_position[0])
        
        if dist_from_base >= min_distance_from_base and dist_from_wall >= 0.5:
            bulb_position = (bulb_x, bulb_y, bulb_z)
            bulb_xy = (bulb_x, bulb_y)
            break
    
    # Fallback if no valid position found
    if bulb_position is None:
        # Default position far from base
        bulb_xy = (-2.0, -2.0)
        bulb_position = (bulb_xy[0], bulb_xy[1], bulb_z)
        print("Warning: Could not find valid random position, using default")

    # Add tower under the bulb (square column)
    tower_scale = [0.15, 0.15, tower_height]  # width, depth, height
    tower = sg.Cuboid(
        scale=tower_scale,
        pose=sm.SE3(bulb_position[0], bulb_position[1], tower_height / 2.0),
        color=COLOR_GRAY,
    )
    env.add(tower)

    bulb_visual = sg.Sphere(radius=BULB_RADIUS, pose=sm.SE3(*bulb_position), color=COLOR_YELLOW)
    env.add(bulb_visual)
    
    print(f"Environment bounds: {world_bounds}")
    print(f"Bulb spawned at: {bulb_position}")
    print(f"Distance from robot base: {np.hypot(bulb_position[0], bulb_position[1]):.2f}m")

    # Create Frankie robot
    # Start configuration: ready position for arm, base at origin
    # Joints: [base_rot, base_trans, arm_joint1, ..., arm_joint7, gripper_joints...]
    # Use qr configuration for arm, zero for base
    temp_robot = rtb.models.URDF.Frankie()
    n_joints = temp_robot.n  # Get actual number of joints
    
    if hasattr(temp_robot, 'qr') and temp_robot.qr is not None:
        qr_full = temp_robot.qr
        # qr has 9 joints: [base_rot, base_trans, arm_joint1, ..., arm_joint7]
        # If robot has more joints (gripper), pad with zeros
        if len(qr_full) < n_joints:
            start_config = np.zeros(n_joints)
            start_config[:len(qr_full)] = qr_full
        else:
            start_config = qr_full[:n_joints].copy()
        start_config[0] = 0.0  # Reset base rotation
        start_config[1] = 0.0  # Reset base translation
    else:
        # Default ready configuration
        start_config = np.zeros(n_joints)
        if n_joints >= 9:
            start_config[2:9] = [0, -0.3, 0, -2.2, 0, 2.0, np.pi / 4]
    start_base_pose = (0.0, 0.0, 0.0)  # x, y, theta
    
    frankie_agent = FrankieAgent("frankie", start_config, start_base_pose)
    frankie_agent.register(env)
    env.step(0.0)

    # Controller configuration
    controller_params = FrankieControllerParams(
        linear_velocity_gain=0.7,  # higher = faster, less smooth
        angular_velocity_gain=2.5, # higher = turns quicker, can oscillate
        max_linear_velocity=0.6,   # absolute limit on forward speed of the base [m/s]
        max_angular_velocity=2.0,  # absolute limit on rotational speed of the base [rad/s]
        base_nav_tolerance=0.10,   # Slightly tighter stop radius
        arm_gain=3.0,              # proportional gain on Cartesian error for the arm (higher = faster EE motion)
        pinv_damping=0.05,         # damping used in the Jacobian pseudo-inverse (higher = more stable but less accurate)
        q_dot_limit=1.5,           # absolute joint-velocity limit for each arm joint [rad/s]
        pos_tolerance=0.12,        # Cartesian distance considered "close enough" to a target point [m]
        screw_rotations=2.0,       # how many full 360° turns the EE performs while screwing the bulb
        grasp_height_offset=0.1,   # vertical offset above the bulb center used for grasping [m]
        approach_distance=0.8,     # base–goal distance at which we stop driving the base and switch to arm-only control [m]
        wall_stop_distance=0.6,    # how far in front of the wall the base stops before using only the arm [m]
    )
    
    controller = FrankieController(controller_params)
    controller.set_bulb_position(bulb_position)
    controller.set_wall_fixture(
        fixture_position, 
        orientation=0.0, 
        wall_x=wall_position[0],
        wall_thickness=wall_size[0]  # Pass wall thickness for collision checking
    )
    controller.params.start_position = (0.0, 0.0)  # Return to origin
    controller.start_task()

    # Data recording
    time_log = []
    state_log = []
    base_pos_log = []
    ee_pos_log = []
    dist_to_bulb_log = []
    dist_to_fixture_log = []
    base_vel_log = []
    arm_vel_norm_log = []

    # Main simulation loop
    steps = int(simulation_time / dt)
    task_complete = False
    
    print("Starting pick-and-place task...")
    print(f"Bulb position: {bulb_position}")
    print(f"Fixture position: {fixture_position}")

    for k in range(steps):
        t = k * dt

        # Get current states
        base_state = frankie_agent.base_state()
        robot = frankie_agent._robot

        # Compute control
        qdot, base_cmd, current_state = controller.compute_control(robot, base_state)

        # Apply control
        frankie_agent.apply_velocity_cmd(qdot, base_cmd)

        # Get end-effector position
        T_ee = robot.fkine(robot.q)
        ee_pos = np.asarray(T_ee.t, dtype=float).reshape(3)

        # Compute metrics
        dist_to_bulb = float(np.linalg.norm(ee_pos - np.array(bulb_position)))
        dist_to_fixture = float(np.linalg.norm(ee_pos - np.array(fixture_position)))
        base_vel = float(np.linalg.norm([base_cmd[0] if base_cmd else 0.0, base_cmd[1] if base_cmd else 0.0]))
        arm_vel_norm = float(np.linalg.norm(qdot[2:]))  # Arm joints only

        # Log data
        time_log.append(t)
        state_log.append(current_state.value)
        base_pos_log.append(base_state.copy())
        ee_pos_log.append(ee_pos.copy())
        dist_to_bulb_log.append(dist_to_bulb)
        dist_to_fixture_log.append(dist_to_fixture)
        base_vel_log.append(base_vel)
        arm_vel_norm_log.append(arm_vel_norm)

        # Update bulb visual position if grasped (simplified - just hide it)
        if current_state in [TaskState.TRANSPORT_TO_WALL, TaskState.APPROACH_WALL, TaskState.SCREW_BULB]:
            # Move bulb visual to end-effector position
            bulb_visual.T = sm.SE3(*ee_pos)

        # Check task completion
        if controller.is_task_complete() and not task_complete:
            task_complete = True
            print(f"Task completed at t={t:.2f}s")

        # State transition logging
        if k > 0 and state_log[-1] != state_log[-2]:
            print(f"[t={t:.2f}s] State: {current_state.value}")
            if current_state.value == "navigate_to_bulb":
                dist_xy = np.hypot(bulb_position[0] - base_state[0], bulb_position[1] - base_state[1])
                print(f"  Base pos: ({base_state[0]:.2f}, {base_state[1]:.2f}), "
                      f"Bulb pos: ({bulb_position[0]:.2f}, {bulb_position[1]:.2f}), "
                      f"Distance: {dist_xy:.2f}m")

        env.step(dt)

    # Cleanup
    env.close()

    # Convert logs to arrays
    time_log = np.array(time_log)
    base_pos_log = np.array(base_pos_log)
    ee_pos_log = np.array(ee_pos_log)
    dist_to_bulb_log = np.array(dist_to_bulb_log)
    dist_to_fixture_log = np.array(dist_to_fixture_log)
    base_vel_log = np.array(base_vel_log)
    arm_vel_norm_log = np.array(arm_vel_norm_log)

    # Plot results
    fig, axs = plt.subplots(4, 1, figsize=(12, 14), sharex=True)
    fig.suptitle("Frankie Pick-and-Place Task Metrics", fontsize=14)

    # Task state
    state_numeric = [list(TaskState).index(TaskState(s)) for s in state_log]
    axs[0].plot(time_log, state_numeric, 'o-', markersize=3, label="State")
    axs[0].set_ylabel("Task State")
    axs[0].set_yticks(range(len(TaskState)))
    axs[0].set_yticklabels([s.value for s in TaskState])
    axs[0].grid(True)
    axs[0].legend()

    # Distances
    axs[1].plot(time_log, dist_to_bulb_log, 'r', label="EE→Bulb")
    axs[1].plot(time_log, dist_to_fixture_log, 'b', label="EE→Fixture")
    axs[1].set_ylabel("Distance [m]")
    axs[1].legend()
    axs[1].grid(True)

    # Base position trajectory
    axs[2].plot(time_log, base_pos_log[:, 0], label="Base x")
    axs[2].plot(time_log, base_pos_log[:, 1], label="Base y")
    axs[2].set_ylabel("Base Position [m]")
    axs[2].legend()
    axs[2].grid(True)

    # Velocities
    axs[3].plot(time_log, base_vel_log, 'g', label="Base velocity")
    axs[3].plot(time_log, arm_vel_norm_log, 'm', label="Arm velocity norm")
    axs[3].set_xlabel("Time [s]")
    axs[3].set_ylabel("Velocity [m/s or rad/s]")
    axs[3].legend()
    axs[3].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig("frankie_pick_and_place_metrics.png", dpi=150)
    print("Saved plot to frankie_pick_and_place_metrics.png")

    # Print summary
    print("\n=== Task Summary ===")
    print(f"Final state: {state_log[-1]}")
    print(f"Task completed: {task_complete}")
    print(f"Final base position: ({base_pos_log[-1, 0]:.2f}, {base_pos_log[-1, 1]:.2f})")
    print(f"Final EE position: ({ee_pos_log[-1, 0]:.2f}, {ee_pos_log[-1, 1]:.2f}, {ee_pos_log[-1, 2]:.2f})")


if __name__ == "__main__":
    main()

