from models import *
from models.base import db
from sqlalchemy.exc import IntegrityError
from routes._relationships_service import assign_project_to_user, remove_user_from_project, assign_task_to_user, remove_task_from_user


def is_error_response(response):
    return isinstance(response, tuple) and 'error' in response[0]


def get_all_users():
    users = db.session.query(User).all()

    return [{
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'last_name': user.last_name
    } for user in users]

def get_specific_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return {'error': f'User {user_id} not found'}, 404
    else:
        return {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'last_name': user.last_name
        }

def get_specific_user_tasks(user_id):
    request_user = get_specific_user(user_id)

    if is_error_response(request_user):
        return request_user

    user_tasks = db.session.query(UserTask).filter_by(user_id=user_id).all()
    task_ids = [ut.task_id for ut in user_tasks]
    task_id_to_work_hours = {ut.task_id: ut.work_hours for ut in user_tasks}

    tasks = db.session.query(Task).filter(Task.id.in_(task_ids)).all()

    return [{
        'id': task.id,
        'name': task.name,
        'location': task.location,
        'start_date': task.start_date.isoformat() if task.start_date else None,
        'end_date': task.end_date.isoformat() if task.end_date else None,
        'actual_cost': task.actual_cost,
        'budget': task.budget,
        'project_id': task.project_id,
        'status': task.status,
        'priority': task.priority,
        'work_hours': task_id_to_work_hours.get(task.id)
    } for task in tasks]


def get_specific_user_projects(user_id):
    request_user = get_specific_user(user_id)
    if is_error_response(request_user):
        return request_user
    else:
        user_projects = db.session.query(UserProject).filter_by(user_id=user_id).all()
        project_ids = [up.project_id for up in user_projects]
        project_id_to_role = {up.project_id: up.role for up in user_projects}

        projects = db.session.query(Project).filter(Project.id.in_(project_ids)).all()

        return [{
            'id': project.id,
            'name': project.name,
            'project_type': project.project_type,
            'project_status': project.project_status,
            'role': project_id_to_role.get(project.id)
    } for project in projects]

def add_user(new_user, keys_ignored=False):
    try:
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id
        user_added = get_specific_user(user_id)
        response = {
            'message': 'User created successfully',
            'user': user_added
        }
        if keys_ignored:
            response['warning'] = f'These fields were ignored: {keys_ignored}'
        return response, 201

    except IntegrityError as e:
        db.session.rollback()  # delete the session
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400

def modify_user(user_id, new_data, field_to_update, keys_ignored=False):
    user = db.session.get(User, user_id)
    if not user:
        return {'error': f'User {user_id} not found'}, 404
    else:
        if len(field_to_update) > 0:
            for field in field_to_update:
                setattr(user, field, new_data[field])
        else:
            return {'warning': f'No valid fields provided'}, 400

        try:
            db.session.commit()
            response = {'message': f'User {user_id} updated successfully'}
            if keys_ignored:
                response['warning'] = f'These fields were ignored: {keys_ignored}'
            return response, 201

        except IntegrityError as e:
            db.session.rollback()  # delete the session
            return {
                'error': 'Database integrity error',
                'message': str(e.orig)
            }, 400

def remove_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {'error': f'User {user_id} does not exist'}, 404

    try:
        for task in user.user_tasks:
            db.session.delete(task)
        for project in user.user_projects:
            db.session.delete(project)
        db.session.delete(user)

        db.session.commit()
        return {'message': f'User {user_id} deleted successfully'}, 200

    except IntegrityError as e:
        db.session.rollback()
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400

########################################################################################################################

def add_user_project(project_id, user_id, user_role, keys_ignored=False):
    return assign_project_to_user(project_id, user_id, user_role, keys_ignored)

def remove_user_project(project_id, user_id):
    return remove_user_from_project(project_id, user_id)

########################################################################################################################

def add_user_task(task_id, user_id, work_hours, keys_ignored=False):
    return assign_task_to_user(task_id, user_id, work_hours, keys_ignored)

def remove_user_task(task_id, user_id):
    return remove_task_from_user(task_id, user_id)