"""
Frankie Robot Controller
Combines mobile base (unicycle-like) and arm control for pick-and-place tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Optional, Sequence, Tuple
import numpy as np
import roboticstoolbox as rtb
import spatialmath as sm


# Helper functions
def _wrap_angle(angle: float) -> float:
    """Wrap an angle to the [-pi, pi] interval."""
    return (angle + np.pi) % (2 * np.pi) - np.pi


def _np3(v: Iterable[float]) -> np.ndarray:
    """Return *v* as a 3-element float array."""
    return np.asarray(list(v), dtype=float).reshape(3)


def damped_pseudoinverse(J: np.ndarray, pinv_damping: float) -> np.ndarray:
    """Damped least-squares pseudoinverse for a position-only Jacobian."""
    m, _ = J.shape
    return J.T @ np.linalg.inv(J @ J.T + pinv_damping * np.eye(m))


# Task states
class TaskState(Enum):
    """States for the pick-and-place task."""
    IDLE = "idle"
    NAVIGATE_TO_BULB = "navigate_to_bulb"
    APPROACH_BULB = "approach_bulb"
    GRASP_BULB = "grasp_bulb"
    TRANSPORT_TO_WALL = "transport_to_wall"
    STOP_IN_FRONT_OF_WALL = "stop_in_front_of_wall"
    APPROACH_WALL = "approach_wall"
    SCREW_BULB = "screw_bulb"
    RETURN_TO_START = "return_to_start"
    RESET = "reset"


# Controller parameters
@dataclass
class FrankieControllerParams:
    """Tunable parameters for Frankie controller."""

    # Mobile base parameters (unicycle controller)
    linear_velocity_gain: float = 0.5      # how strongly the base moves forward toward the goal (higher = faster, less smooth)
    angular_velocity_gain: float = 1.0     # how strongly the base turns to face the goal (higher = turns quicker, can oscillate)
    max_linear_velocity: float = 0.5       # absolute limit on forward speed of the base [m/s]
    max_angular_velocity: float = 1.5      # absolute limit on rotational speed of the base [rad/s]
    base_nav_tolerance: float = 0.15       # distance threshold at which the base considers itself "at" a target point [m]

    # Arm parameters (resolved-rate control)
    arm_gain: float = 1.0                  # proportional gain on Cartesian error for the arm (higher = faster EE motion)
    pinv_damping: float = 0.3              # damping used in the Jacobian pseudo-inverse (higher = more stable but less accurate)
    q_dot_limit: float = 1.5               # absolute joint-velocity limit for each arm joint [rad/s]
    pos_tolerance: float = 2.5e-2          # Cartesian distance considered "close enough" to a target point [m]
    screw_rotations: float = 2.0           # how many full 360° turns the EE performs while screwing the bulb

    # Task-level parameters (behaviour of the sequence)
    grasp_height_offset: float = 0.1       # vertical offset above the bulb center used for grasping [m]
    approach_distance: float = 0.6         # base–goal distance at which we stop driving the base and switch to arm-only control [m]
    wall_stop_distance: float = 0.6        # how far in front of the wall the base stops before using only the arm [m]
    start_position: Tuple[float, float] = (0.0, 0.0)  # (x,y) base position considered the "home" pose for return
    wall_thickness: float = 0.1            # physical thickness of the wall model, used to position the target marker [m]
    arm_safety_margin: float = 0.02        # safety gap to keep the EE away from the wall surface during approach [m]


# Main controller
class FrankieController:
    """
    Controller for Frankie robot combining mobile base and arm control.
    
    The controller manages a state machine to execute pick-and-place tasks:
    1. Navigate mobile base to lightbulb location
    2. Approach and grasp the bulb with the arm
    3. Transport to wall location
    4. Screw the bulb into the fixture
    5. Reset to ready position
    """

    def __init__(self, params: FrankieControllerParams) -> None:
        self.params = params
        self.state = TaskState.IDLE
        
        # Task targets
        self.bulb_position: Optional[np.ndarray] = None
        self.wall_fixture_position: Optional[np.ndarray] = None
        self.wall_fixture_orientation: Optional[float] = None  # rotation around screw axis
        self.wall_x_position: Optional[float] = None  # Wall x-coordinate for collision avoidance
        self.wall_surface_x: Optional[float] = None  # Wall surface x-coordinate (facing robot)
        
        # Internal state
        self._screw_angle: float = 0.0
        self._screw_target_angle: float = 0.0
        self._grasped: bool = False
        self._stop_position: Optional[Tuple[float, float]] = None  # Position in front of wall

    # State management
    def set_bulb_position(self, position: Tuple[float, float, float]) -> None:
        """Set the target lightbulb position."""
        self.bulb_position = _np3(position)

    def set_wall_fixture(self, position: Tuple[float, float, float], orientation: float = 0.0, wall_x: Optional[float] = None, wall_thickness: Optional[float] = None) -> None:
        """Set the wall fixture position and orientation."""
        self.wall_fixture_position = _np3(position)
        self.wall_fixture_orientation = float(orientation)
        if wall_x is not None:
            self.wall_x_position = float(wall_x)
            # Calculate wall surface position (wall center - half thickness, facing robot)
            if wall_thickness is not None:
                self.wall_surface_x = wall_x - (wall_thickness / 2.0)
            else:
                self.wall_surface_x = wall_x - (self.params.wall_thickness / 2.0)
            # Calculate stop position in front of wall
            stop_x = wall_x - self.params.wall_stop_distance
            stop_y = float(position[1])  # Same y as fixture
            self._stop_position = (stop_x, stop_y)

    def start_task(self) -> None:
        """Start the pick-and-place task."""
        if self.bulb_position is None:
            raise ValueError("Bulb position must be set before starting task.")
        if self.wall_fixture_position is None:
            raise ValueError("Wall fixture position must be set before starting task.")
        self.state = TaskState.NAVIGATE_TO_BULB
        self._grasped = False
        self._screw_angle = 0.0

    def reset_task(self) -> None:
        """Reset the task to idle state."""
        self.state = TaskState.IDLE
        self._grasped = False
        self._screw_angle = 0.0

    # Mobile base control (unicycle-like)
    def _compute_base_control(
        self, 
        base_state: Sequence[float], 
        target_xy: Tuple[float, float]
    ) -> Tuple[float, float]:
        """
        Compute unicycle control to reach target (x, y).
        Returns (linear_velocity, angular_velocity).
        """
        x = float(base_state[0])
        y = float(base_state[1])
        theta = float(base_state[2])
        gx, gy = float(target_xy[0]), float(target_xy[1])

        dx = gx - x
        dy = gy - y
        rho = float(np.hypot(dx, dy))
        theta_star = float(np.arctan2(dy, dx))
        heading_err = _wrap_angle(theta_star - theta)

        v = self.params.linear_velocity_gain * rho
        omega = self.params.angular_velocity_gain * heading_err

        # Clip to limits
        v = float(np.clip(v, -self.params.max_linear_velocity, self.params.max_linear_velocity))
        omega = float(np.clip(omega, -self.params.max_angular_velocity, self.params.max_angular_velocity))
        
        return v, omega

    # Arm control
    def _compute_arm_control(
        self,
        robot: rtb.ERobot,
        target_position: np.ndarray,
        target_orientation: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute arm joint velocities to reach target position.
        Optionally includes rotation around z-axis for screwing.
        Returns (qdot, position_error).
        """
        q = robot.q
        T_ee = robot.fkine(q)
        p_ee = np.asarray(T_ee.t, dtype=float).reshape(3)

        # Position error
        e_pos = target_position - p_ee

        # Orientation control for screwing (if needed)
        if target_orientation is not None:
            # Get current orientation (z-axis rotation)
            current_rot = float(np.arctan2(T_ee.R[1, 0], T_ee.R[0, 0]))
            e_rot = _wrap_angle(target_orientation - current_rot)
        else:
            e_rot = 0.0

        # Use position Jacobian (first 3 rows)
        Jpos = robot.jacob0(q)[:3, :]
        Jpinv = damped_pseudoinverse(Jpos, self.params.pinv_damping)

        # Resolved-rate control
        qdot = (self.params.arm_gain * (Jpinv @ e_pos.reshape(3, 1))).ravel()
        
        # Add rotation control if needed (use end-effector joint, not base joint)
        if abs(e_rot) > 0.01 and target_orientation is not None:
            # Use the last joint in q as the end-effector joint
            ee_idx = robot.n - 1
            qdot[ee_idx] += 0.5 * e_rot

        # Clip joint velocities
        qdot = np.clip(qdot, -self.params.q_dot_limit, self.params.q_dot_limit)
        
        return qdot, e_pos

    # Main control computation
    def compute_control(
        self,
        robot: rtb.ERobot,
        base_state: Optional[Sequence[float]] = None
    ) -> Tuple[np.ndarray, Optional[Tuple[float, float]], TaskState]:
        """
        Compute control commands for both mobile base and arm.
        
        Returns:
            - qdot: Arm joint velocities (9 elements: 2 base + 7 arm)
            - base_cmd: (linear_velocity, angular_velocity) for mobile base, or None
            - current_state: Current task state
        """
        if self.state == TaskState.IDLE:
            # Return zero velocities
            qdot = np.zeros(robot.n)
            return qdot, None, self.state

        # Get current robot configuration
        q = robot.q
        
        # Extract base state - use provided base_state or infer from robot base transform
        if base_state is None:
            # Infer from robot base transform
            T_base = robot.base if hasattr(robot, 'base') else sm.SE3()
            base_pos = np.asarray(T_base.t, dtype=float).reshape(3)
            base_x = float(base_pos[0])
            base_y = float(base_pos[1])
            if hasattr(T_base, 'R') and T_base.R is not None:
                base_theta = float(np.arctan2(T_base.R[1, 0], T_base.R[0, 0]))
            else:
                base_theta = 0.0
            base_state = [base_x, base_y, base_theta]

        # State machine
        if self.state == TaskState.NAVIGATE_TO_BULB:
            # Navigate mobile base to bulb location
            if self.bulb_position is None:
                self.state = TaskState.IDLE
                return np.zeros(robot.n), None, self.state

            # Check if close enough to switch to arm control
            dist_to_bulb = float(np.hypot(
                self.bulb_position[0] - base_state[0],
                self.bulb_position[1] - base_state[1]
            ))

            if dist_to_bulb <= self.params.approach_distance:
                self.state = TaskState.APPROACH_BULB
            else:
                # Control mobile base using unicycle model
                v, omega = self._compute_base_control(
                    base_state,
                    (float(self.bulb_position[0]), float(self.bulb_position[1]))
                )
                # Convert unicycle commands to joint velocities
                # Joint 0: rotation (omega)
                # Joint 1: translation along x (v * cos(theta) in base frame, simplified to v)
                qdot = np.zeros(robot.n)
                qdot[0] = omega  # base rotation
                qdot[1] = v  # base translation (simplified - assumes aligned with x)
                return qdot, (v, omega), self.state

        if self.state == TaskState.APPROACH_BULB:
            # Position arm to grasp bulb: move EE above bulb at a safe Z
            if self.bulb_position is None:
                self.state = TaskState.IDLE
                return np.zeros(robot.n), None, self.state

            grasp_target = self.bulb_position.copy()
            safe_z = max(float(self.bulb_position[2]) + self.params.grasp_height_offset, 0.35)
            grasp_target[2] = safe_z

            # Compute arm control (only arm joints, base joints set to zero)
            qdot, e_pos = self._compute_arm_control(robot, grasp_target)
            qdot[0] = 0.0
            qdot[1] = 0.0

            # When close enough above bulb, mark as grasped and proceed
            if float(np.linalg.norm(e_pos)) <= 0.04:  # 4 cm radius
                self.state = TaskState.GRASP_BULB
                self._grasped = True

            return qdot, None, self.state

        if self.state == TaskState.GRASP_BULB:
            # Maintain pose above bulb (simulate grasp), then go to transport
            if self.bulb_position is None:
                self.state = TaskState.IDLE
                return np.zeros(robot.n), None, self.state

            grasp_target = self.bulb_position.copy()
            safe_z = max(float(self.bulb_position[2]) + self.params.grasp_height_offset, 0.35)
            grasp_target[2] = safe_z

            qdot, _ = self._compute_arm_control(robot, grasp_target)
            qdot[0] = 0.0
            qdot[1] = 0.0

            # Immediately start transporting once we stabilise the grasp pose
            self.state = TaskState.TRANSPORT_TO_WALL
            return qdot, None, self.state

        if self.state == TaskState.TRANSPORT_TO_WALL:
            # Move base toward stop position in front of wall; freeze arm joints
            if self._stop_position is None:
                if self.wall_fixture_position is None:
                    self.state = TaskState.IDLE
                    return np.zeros(robot.n), None, self.state
                stop_x = self.wall_fixture_position[0] - self.params.wall_stop_distance
                stop_y = self.wall_fixture_position[1]
                self._stop_position = (stop_x, stop_y)

            dist_to_stop = float(np.hypot(
                self._stop_position[0] - base_state[0],
                self._stop_position[1] - base_state[1]
            ))

            if dist_to_stop <= self.params.base_nav_tolerance:
                self.state = TaskState.STOP_IN_FRONT_OF_WALL
                return np.zeros(robot.n), None, self.state

            v, omega = self._compute_base_control(base_state, self._stop_position)
            qdot = np.zeros(robot.n)
            qdot[0] = omega
            qdot[1] = v
            # arm joints unchanged (hold grasp pose)
            return qdot, (v, omega), self.state

        if self.state == TaskState.STOP_IN_FRONT_OF_WALL:
            # Base has reached stop point; keep everything still, then start wall approach
            qdot = np.zeros(robot.n)
            self.state = TaskState.APPROACH_WALL
            return qdot, None, self.state

        if self.state == TaskState.APPROACH_WALL:
            # Position arm to wall fixture
            if self.wall_fixture_position is None:
                self.state = TaskState.IDLE
                return np.zeros(robot.n), None, self.state

            # Directly target the fixture position (red marker)
            target_pos = self.wall_fixture_position.copy()

            # Compute arm control to target position
            qdot, e_pos = self._compute_arm_control(robot, target_pos)
            qdot[0] = 0.0
            qdot[1] = 0.0

            # Check if close enough to screw (considering the constrained position)
            if float(np.linalg.norm(e_pos)) <= self.params.pos_tolerance:
                self.state = TaskState.SCREW_BULB
                self._screw_target_angle = self.params.screw_rotations * 2 * np.pi

            return qdot, None, self.state

        if self.state == TaskState.SCREW_BULB:
            # Rotate end-effector (last joint) to screw bulb, keep base fixed
            if self.wall_fixture_position is None:
                self.state = TaskState.IDLE
                return np.zeros(robot.n), None, self.state

            # Maintain end-effector at fixture position while rotating
            target_pos = self.wall_fixture_position.copy()
            qdot, _ = self._compute_arm_control(robot, target_pos)
            # Ensure base joints are zeroed: only arm (end-effector) will rotate
            qdot[0] = 0.0
            qdot[1] = 0.0

            # Add screwing rotation using the end-effector joint (last index)
            ee_idx = robot.n - 1
            if self._screw_angle < self._screw_target_angle:
                screw_rate = 0.5  # rad/s
                self._screw_angle += screw_rate * 0.05  # assuming dt=0.05
                qdot[ee_idx] = screw_rate
            else:
                # Screwing complete, return to start position
                self.state = TaskState.RETURN_TO_START
                self._grasped = False

            return qdot, None, self.state

        if self.state == TaskState.RETURN_TO_START:
            # Navigate back to starting position
            start_x, start_y = self.params.start_position
            
            # Check distance to start
            dist_to_start = float(np.hypot(
                start_x - base_state[0],
                start_y - base_state[1]
            ))

            if dist_to_start <= self.params.base_nav_tolerance:
                # Reached start position, now reset arm
                self.state = TaskState.RESET
            else:
                # Control mobile base to start position
                v, omega = self._compute_base_control(
                    base_state,
                    (start_x, start_y)
                )
                qdot = np.zeros(robot.n)
                qdot[0] = omega
                qdot[1] = v
                # Return arm to ready position while moving
                if hasattr(robot, 'qr'):
                    ready_config = robot.qr
                else:
                    ready_config = np.zeros(robot.n)
                q = robot.q
                e_q = ready_config - q
                arm_qdot = self.params.arm_gain * e_q
                arm_qdot = np.clip(arm_qdot, -self.params.q_dot_limit, self.params.q_dot_limit)
                qdot[2:] = arm_qdot[2:]  # Only arm joints
                return qdot, (v, omega), self.state

        if self.state == TaskState.RESET:
            # Return arm to ready position (base already at start)
            if hasattr(robot, 'qr'):
                ready_config = robot.qr
            else:
                ready_config = np.zeros(robot.n)

            q = robot.q
            e_q = ready_config - q
            qdot = self.params.arm_gain * e_q
            qdot = np.clip(qdot, -self.params.q_dot_limit, self.params.q_dot_limit)
            
            # Zero base joints during reset
            qdot[0] = 0.0
            qdot[1] = 0.0

            # Check if reset complete
            if float(np.linalg.norm(e_q)) < 0.1:
                self.state = TaskState.IDLE

            return qdot, None, self.state

        # Default: return zero
        return np.zeros(robot.n), None, self.state

    def is_task_complete(self) -> bool:
        """Check if task is complete (back to idle after screwing)."""
        return self.state == TaskState.IDLE and self._grasped == False

