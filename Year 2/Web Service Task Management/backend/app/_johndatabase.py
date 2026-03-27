import pandas as pd
from datetime import datetime
import random
from models import *

def delete_all_data(db):
    db.session.query(UserTask).delete()
    db.session.query(Task).delete()
    db.session.query(User).delete()
    db.session.query(Project).delete()
    db.session.query(ProjectStatus).delete()
    db.session.query(TaskStatus).delete()
    db.session.query(ProjectType).delete()
    db.session.query(Priority).delete()
    db.session.query(Role).delete()
    db.session.commit()
    print("All data has been successfully deleted!")

def populate_database(csv_file, db):
    df = pd.read_csv(csv_file)

    # Track which projects have been added already
    added_projects = set()

    # Populate project status
    for status in df['Project Status'].unique():
        existing_status = db.session.query(ProjectStatus).filter_by(status=status).first()
        if not existing_status:
            project_status = ProjectStatus(status=status)
            db.session.add(project_status)

    # Populate task status
    for status in df['Task Status'].unique():
        existing_status = db.session.query(TaskStatus).filter_by(status=status).first()
        if not existing_status:
            task_status = TaskStatus(status=status)
            db.session.add(task_status)

    # Populate Project type
    for ptype in df['Project Type'].unique():
        existing_type = db.session.query(ProjectType).filter_by(type=ptype).first()
        if not existing_type:
            project_type = ProjectType(type=ptype)
            db.session.add(project_type)

    # Populate priority
    for level in df['Priority'].unique():
        existing_priority = db.session.query(Priority).filter_by(level=level).first()
        if not existing_priority:
            priority = Priority(level=level)
            db.session.add(priority)

    # Populate role
    for r in ["Admin", "Normal"]:
        role = Role(name=r)
        db.session.add(role)

    db.session.commit()

    user_id_counter = 1
    # Project and Task population
    for index, row in df.iterrows():
        start_date = datetime.strptime(row['Start Date'], "%d/%m/%Y")
        end_date = datetime.strptime(row['End Date'], "%d/%m/%Y") if row['End Date'] else None

        project_name = row['Project Name']
        if project_name not in added_projects:
            existing_project = db.session.query(Project).filter_by(name=project_name).first()

            if not existing_project:
                project = Project(
                    name=project_name,
                    project_type=row['Project Type'],
                    project_status=row['Project Status']
                )
                db.session.add(project)
                db.session.commit()
                added_projects.add(project_name)
            else:
                added_projects.add(project_name)
                project = existing_project

        else:
            project = db.session.query(Project).filter_by(name=project_name).first()

        task = Task(
            name=row['Task Name'],
            location=row['Location'],
            start_date=start_date,
            end_date=end_date,
            actual_cost=row['Actual Cost'],
            budget=row['Budget'],
            project_id=project.id,
            status=row['Task Status'],
            priority=row['Priority']
        )
        db.session.add(task)


        #Populate Users
        name = row['Assigned To']
        existing_user = db.session.query(User).filter_by(name=name).first()

        if not existing_user:
            # Create new user with incrementing ID and random last name
            last_name = random.choice(
                ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin"])
            user = User(
                id=user_id_counter,
                name=name,
                username=str(user_id_counter) + "-" + str(name),
                last_name=last_name,
            )

            db.session.add(user)
            db.session.commit()
            user_id_counter += 1  # Increment user ID for next user
        else:
            user = existing_user

        # Check if the UserProject already exists
        existing_user_project = db.session.query(UserProject).filter_by(user_id=user.id,
                                                                        project_id=project.id).first()
        if not existing_user_project:
            # Assign User to Project
            user_project = UserProject(user_id=user.id, project_id=project.id,
                                       role=random.choice(["Admin", "Normal"]))
            db.session.add(user_project)

        # Assign User to Task
        user_task = UserTask(user_id=user.id, task_id=task.id, work_hours=row['Hours Spent'])
        db.session.add(user_task)

    db.session.commit()
    print("Database populated successfully!")