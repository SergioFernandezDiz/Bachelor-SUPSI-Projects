from models import *
from models.base import db
from sqlalchemy.exc import IntegrityError
from routes._relationships_service import assign_project_to_user, remove_user_from_project


def is_error_response(response):
    return isinstance(response, tuple) and 'error' in response[0]


def get_all_projects():
    projects = db.session.query(Project).all()
    return [{
        'id': project.id,
        'name': project.name,
        'project_type': project.project_type,
        'project_status': project.project_status
    }for project in projects]

def get_all_status():
    status = db.session.query(ProjectStatus).all()
    return [{
        'status': s.status,
        'description': s.description
    } for s in status]

def get_all_types():
    types = db.session.query(ProjectType).all()
    return [{
        'type': t.type,
        'description': t.description
    }for t in types]

def get_specific_project(project_id):
    project = db.session.get(Project, project_id)

    if not project:
        return {'error': f'Project {project_id} not found'}, 404
    else:
        return {
        'id': project.id,
        'name': project.name,
        'project_type': project.project_type,
        'project_status': project.project_status
    }

def get_specific_project_users(project_id):
    request_project = get_specific_project(project_id)
    if is_error_response(request_project):
        return request_project

    project_users = db.session.query(UserProject).filter_by(project_id=project_id).all()
    user_ids = [pu.user_id for pu in project_users]
    user_id_to_role = {pu.user_id: pu.role for pu in project_users}

    users = db.session.query(User).filter(User.id.in_(user_ids)).all()

    return [{
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'last_name': user.last_name,
        'role': user_id_to_role.get(user.id)
    } for user in users]

def get_specific_project_tasks(project_id):
    request_project = get_specific_project(project_id)

    if is_error_response(request_project):
        return request_project

    project_tasks = db.session.query(Task).filter_by(project_id=project_id).all()
    tasks_ids = [pt.id for pt in project_tasks]
    user_tasks = db.session.query(UserTask).filter(UserTask.task_id.in_(tasks_ids)).all()

    task_id_to_work_hours = {}
    for ut in user_tasks:
        if ut.task_id in task_id_to_work_hours:
            task_id_to_work_hours[ut.task_id] += ut.work_hours
        else:
            task_id_to_work_hours[ut.task_id] = ut.work_hours

    tasks = db.session.query(Task).filter(Task.id.in_(tasks_ids)).all()

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

##############################################################################

def add_project(data, keys_ignored=False):
    # verify foreign keys
    type_exists = db.session.query(ProjectType).filter_by(type=data['project_type']).first()
    status_exists = db.session.query(ProjectStatus).filter_by(status=data['project_status']).first()

    if not type_exists:
        return {'error': f'Invalid project_type',
                'message': f'{data["project_type"]} not supported'}, 404
    if not status_exists:
        return {'error': f'Invalid project_status',
                'message': f'{data["project_status"]} not supported'}, 404

    new_project = Project(
        name=data['name'],
        project_type=data['project_type'],
        project_status=data['project_status']
    )

    try:
        db.session.add(new_project)
        db.session.commit()
        project_id = new_project.id
        project_added = get_specific_project(project_id)
        response = {
            'message': 'Project created successfully',
            'project': project_added
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

def modify_project(project_id, new_data, field_to_update, keys_ignored=False):
    project = db.session.get(Project, project_id)
    if not project:
        return {'error': f'Project {project_id} not found'}, 404
    else:
        # verify foreign keys
        if 'project_type' in field_to_update:
            type_exists = db.session.query(ProjectType).filter_by(type=new_data['project_type']).first()
            if not type_exists:
                return {'error': f'Invalid project_type',
                        'message': f'{new_data["project_type"]} not supported'}, 404

        if 'project_status' in field_to_update:
            status_exists = db.session.query(ProjectStatus).filter_by(status=new_data['project_status']).first()
            if not status_exists:
                return {'error': f'Invalid project_status',
                        'message': f'{new_data["project_status"]} not supported'}, 404

        if len(field_to_update) > 0:
            for field in field_to_update:
                setattr(project, field, new_data[field])
        else:
            return {'warning': 'No valid fields provided'}, 400

        try:
            db.session.commit()
            response = {'message': f'Project {project_id} updated successfully'}
            if keys_ignored:
                response['warning'] = f'These fields were ignored: {keys_ignored}'
            return response, 201

        except IntegrityError as e:
            db.session.rollback()  # delete the session
            return {
                'error': 'Database integrity error',
                'message': str(e.orig)
            }, 400


def remove_project(project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return {'error': f'Project {project_id} does not exist'}, 404

    try:
        for task in project.tasks:
            for user_task in task.user_tasks:
                db.session.delete(user_task)
            db.session.delete(task)
        for user_project in project.user_projects:
            db.session.delete(user_project)
        db.session.delete(project)

        db.session.commit()
        return {'message': f'Project {project_id} deleted successfully'}, 200

    except IntegrityError as e:
        db.session.rollback()
        return {
            'error': 'Database integrity error',
            'message': str(e.orig)
        }, 400

########################################################################################################################

def add_project_user(project_id, user_id, user_role, keys_ignored=False):
    return assign_project_to_user(project_id, user_id, user_role, keys_ignored)

def remove_project_user(project_id, user_id):
    return remove_user_from_project(project_id, user_id)