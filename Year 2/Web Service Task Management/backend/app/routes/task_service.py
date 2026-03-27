from models import *
from models.base import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from routes._relationships_service import assign_task_to_user, remove_task_from_user

def is_error_response(response):
    return isinstance(response, tuple) and 'error' in response[0]

def parse_datetime(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None

def get_all_tasks():
    tasks = db.session.query(Task).all()
    return [{
        'id': t.id,
        'name': t.name,
        'location': t.location,
        'start_date': t.start_date.isoformat() if t.start_date else None,
        'end_date': t.end_date.isoformat() if t.end_date else None,
        'actual_cost': t.actual_cost,
        'budget': t.budget,
        'project_id': t.project_id,
        'status': t.status,
        'priority': t.priority
    } for t in tasks]

def get_all_status():
    status = db.session.query(TaskStatus).all()
    return [{
        'status': s.status,
        'description': s.description
    }for s in status]

def get_all_priorities():
    priorities = db.session.query(Priority).all()
    return [{
        'level': p.level
    } for p in priorities]

def get_specific_task(task_id):
    task = db.session.get(Task, task_id)

    if not task:
        return {'error': f'Task {task_id} not found'}, 404
    else:
        return {
        'id': task.id,
        'name': task.name,
        'location': task.location,
        'start_date': task.start_date.isoformat() if task.start_date else None,
        'end_date': task.end_date.isoformat() if task.end_date else None,
        'actual_cost': task.actual_cost,
        'budget': task.budget,
        'project_id': task.project_id,
        'status': task.status,
        'priority': task.priority
    }

def get_specific_task_users(task_id):
    request_task = get_specific_task(task_id)

    if is_error_response(request_task):
        return request_task

    task_users = db.session.query(UserTask).filter_by(task_id=task_id).all()
    user_ids = [tu.user_id for tu in task_users]
    user_id_to_work_hours = {tu.user_id: tu.work_hours for tu in task_users}

    users = db.session.query(User).filter(User.id.in_(user_ids)).all()
    return [{
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'last_name': user.last_name,
        'work_hours': user_id_to_work_hours.get(user.id)
    } for user in users]


def add_task(new_task,keys_ignored = False):

    # Foreign key validation
    project = db.session.query(Project).filter_by(id=new_task.project_id).first()
    if not project:
        return {'error': 'Invalid project_id'}, 404
    if not db.session.query(TaskStatus).filter_by(status=new_task.status).first():
        return {'error': 'Invalid status'}, 404
    if new_task.priority:
        if not db.session.query(Priority).filter_by(level=new_task.priority).first():
            return {'error': 'Invalid priority'}, 404

    try:
        db.session.add(new_task)
        db.session.commit()
        task_id  = new_task.id

        task_added = get_specific_task(task_id)
        response = {
            'message': 'Task created successfully',
            'task': task_added
        }
        if keys_ignored:
            response['warning'] = f'These fields were ignored: {keys_ignored}'
        return response, 201

    except IntegrityError as e:
        db.session.rollback()
        return {'error': 'Database integrity error', 'message': str(e.orig)}, 400


def modify_task(task_id, new_data, field_to_update, keys_ignored=False):
    task = db.session.get(Task, task_id)
    if not task:
        return {'error': f'Task {task_id} not found'}, 404

    # FK validation
    if 'project_id' in new_data:
        if not db.session.query(Project).filter_by(id=new_data['project_id']).first():
            return {'error': 'Invalid project_id'}, 404
    if 'status' in new_data:
        if not db.session.query(TaskStatus).filter_by(status=new_data['status']).first():
            return {'error': 'Invalid status'}, 404
    if 'priority' in new_data and new_data['priority']:
        if not db.session.query(Priority).filter_by(level=new_data['priority']).first():
            return {'error': 'Invalid priority'}, 404

    # Update fields
    for field in field_to_update:
        if field in ['start_date', 'end_date']:
            parsed = parse_datetime(new_data[field])
            if not parsed and new_data[field]:
                return {'error': f'Invalid format for {field}, expected ISO 8601'}, 400
            setattr(task, field, parsed)
        else:
            setattr(task, field, new_data[field])

    try:
        db.session.commit()
        response = {'message': f'Task {task_id} updated successfully'}
        if keys_ignored:
            response['warning'] = f'These fields were ignored: {keys_ignored}'
        return response, 201
    except IntegrityError as e:
        db.session.rollback()
        return {'error': 'Database integrity error', 'message': str(e.orig)}, 400

def remove_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).first()

    if not task:
        return {'error': f'Task {task_id} does not exist'}, 404

    try:
        for user_task in task.user_tasks:
            db.session.delete(user_task)

        db.session.delete(task)
        db.session.commit()

        return {'message': f'Task {task_id} deleted successfully'}, 200

    except IntegrityError as e:
        db.session.rollback()
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400

########################################################################################################################

def add_task_user(task_id, user_id, work_hours, keys_ignored=False):
    return assign_task_to_user(task_id, user_id, work_hours, keys_ignored)

def remove_task_user(task_id, user_id):
    return remove_task_from_user(task_id, user_id)
