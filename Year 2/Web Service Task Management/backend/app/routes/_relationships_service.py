from models import *
from models.base import db
from sqlalchemy.exc import IntegrityError

# many-to-many relationships

# assign a project to a user
def assign_project_to_user(project_id, user_id, user_role, keys_ignored=False):
    project = db.session.get(Project, project_id)
    user = db.session.get(User, user_id)

    if not project:
        return {'error': f'Project {project_id} not found'}, 404
    if not user:
        return {'error': f'User {user_id} not found'}, 404

    # search for duplicates
    project_user_exists = db.session.query(UserProject).filter_by(user_id=user_id, project_id=project_id).first()
    # when a project has the user yet, the role is not updated
    if user_role is None and not project_user_exists:
        user_role = 'Normal'
    elif user_role is None and project_user_exists:
        user_role = project_user_exists.role
    else: # otherwise it's added
        role_exists = db.session.query(Role).filter_by(name=user_role).first()
        if not role_exists:
            return {'error': f'Invalid user_role',
                    'message': f'{user_role} not supported'}, 404
    try:
        if not project_user_exists:
            new_assignment = UserProject(
                user_id=user_id,
                project_id=project_id,
                role=user_role
            )

            db.session.add(new_assignment)
            db.session.commit()
            response = {'message': f'Project {project_id} assigned to User {user_id} successfully'}

        else:
            # update the user's role
            if user_role is not None:
                setattr(project_user_exists, 'role', user_role)
                db.session.commit()
                response = {'message': f'Updated role of User {user_id} in Project {project_id} successfully to {user_role}'}
            else:
                response = {'message': f'Assignment present jet'}, 200

        if keys_ignored:
            response['warning'] = f'These fields were ignored: {keys_ignored}'
        return response, 201

    except IntegrityError as e:
        db.session.rollback()  # delete the session
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400

# remove a user from a project
def remove_user_from_project(project_id, user_id):
    project = db.session.get(Project, project_id)
    user = db.session.get(User, user_id)

    if not project:
        return {'error': f'Project {project_id} not found'}, 404
    if not user:
        return {'error': f'User {user_id} not found'}, 404

    project_user = db.session.query(UserProject).filter_by(user_id=user_id, project_id=project_id).first()
    if not project_user:
        return {'error': f'Project {project_id} is not assigned to User {user_id} yet'}, 404

    try:
        db.session.delete(project_user)
        db.session.commit()
        return {'message': f'User {user_id} deleted successfully from Project {project_id}'}, 200

    except IntegrityError as e:
        db.session.rollback()
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400

########################################################################################################################

# assign a project to a user
def assign_task_to_user(task_id, user_id, work_hours, keys_ignored=False):
    task = db.session.get(Task, task_id)
    user = db.session.get(User, user_id)

    if not task:
        return {'error': f'Task {task_id} not found'}, 404
    if not user:
        return {'error': f'User {user_id} not found'}, 404

    # search for duplicates
    task_user_exists = db.session.query(UserTask).filter_by(user_id=user_id, task_id=task_id).first()
    # when a project has the user yet, the role is not updated
    if work_hours is None:
        work_hours = 0.0
    else: # otherwise it's added
        if work_hours < 0:
            return {'error': f'Invalid work_hours',
                    'message': f'{work_hours} must be positive'}, 404
    try:
        if not task_user_exists:
            new_assignment = UserTask(
                user_id=user_id,
                task_id=task_id,
                work_hours=work_hours
            )

            db.session.add(new_assignment)
            db.session.commit()
            response = {'message': f'Task {task_id} assigned to User {user_id} successfully'}

        else:
            # update the task's work_hours
            if work_hours is not None:
                updated_work_hours = task_user_exists.work_hours + work_hours
                setattr(task_user_exists, 'work_hours', updated_work_hours)
                db.session.commit()
                response = {'message': f'Updated work_hours of Task {task_id} assigned to User {user_id} successfully to {updated_work_hours}'}
            else:
                response = {'message': f'Assignment present jet'}, 200

        if keys_ignored:
            response['warning'] = f'These fields were ignored: {keys_ignored}'
        return response, 201

    except IntegrityError as e:
        db.session.rollback()  # delete the session
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400

# remove a user from a project
def remove_task_from_user(task_id, user_id):
    task = db.session.get(Task, task_id)
    user = db.session.get(User, user_id)

    if not task:
        return {'error': f'Task {task_id} not found'}, 404
    if not user:
        return {'error': f'User {user_id} not found'}, 404

    task_user = db.session.query(UserTask).filter_by(user_id=user_id, task_id=task_id).first()
    if not task_user:
        return {'error': f'Task {task_id} is not assigned to User {user_id} yet'}, 404

    try:
        db.session.delete(task_user)
        db.session.commit()
        return {'message': f'User {user_id} deleted successfully from Task {task_id}'}, 200

    except IntegrityError as e:
        db.session.rollback()
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400
