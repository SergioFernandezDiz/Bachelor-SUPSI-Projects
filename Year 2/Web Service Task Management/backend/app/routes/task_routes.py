from flask import request,Blueprint
from models import *

from datetime import datetime
from routes._utils import check_type_values, check_key_values
from routes.task_service import get_all_tasks,get_specific_task,add_task,get_specific_task_users,modify_task,remove_task,add_task_user,remove_task_user, get_all_status, get_all_priorities


task_endpoints = Blueprint('task_endpoints',__name__, url_prefix='/task')

fields = ['name', 'location', 'start_date', 'end_date', 'actual_cost', 'budget', 'project_id', 'status', 'priority']
key_fields = ['name', 'location', 'start_date', 'project_id', 'status']
float_fields = ['actual_cost', 'budget']
date_fields = ['start_date', 'end_date']
str_fields = ['name', 'location', 'status', 'priority']


def parse_datetime(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None

@task_endpoints.route('/', methods=['GET'])
def get_tasks():
    tasks = get_all_tasks()
    return tasks

@task_endpoints.route('/status', methods=['GET'])
def get_tasks_status():
    status = get_all_status()
    return status

@task_endpoints.route('/priorities', methods=['GET'])
def get_tasks_priorities():
    priorities = get_all_priorities()
    return priorities

@task_endpoints.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_specific_task(task_id)
    return task

@task_endpoints.route('/<int:task_id>/users', methods=['GET'])
def get_task_users(task_id):
    users = get_specific_task_users(task_id)
    return users



###################################################################################
@task_endpoints.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    keys_ignored = False

    # Validate required keys
    key_check = check_key_values(data, key_fields)
    if key_check:
        return key_check

    global fields
    # check for keys not required, then ignored
    if not all(k in fields for k in data):
        keys_ignored = [k for k in data if k not in fields]

    # Type checks
    for fields_group, expected in [
        (str_fields, str),
        (float_fields, float),
        (date_fields, str)
    ]:
        type_check = check_type_values(data, fields_group, expected)
        if type_check:
            return type_check

    # Parse datetime
    start_date = parse_datetime(data['start_date'])
    end_date = parse_datetime(data.get('end_date')) if data.get('end_date') else None

    if not start_date:
        return {'error': 'Invalid start_date format (use ISO 8601)'}, 400

    # Create task
    new_task = Task(
        name=data['name'],
        location=data['location'],
        start_date=start_date,
        end_date=end_date,
        actual_cost=data.get('actual_cost'),
        budget=data.get('budget'),
        project_id=data['project_id'],
        status=data['status'],
        priority=data.get('priority')
    )

    request_creation = add_task(new_task, keys_ignored)
    return request_creation



@task_endpoints.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return {'error': 'Missing required fields',
                'message': 'The request body is empty or missing required fields'
                }, 400

    global fields
    # check for keys not required, then ignored
    keys_ignored = False
    if not all(k in fields for k in data):
        keys_ignored = [k for k in data if k not in fields]

    # type check
    for fields_group, expected_type in [
        (str_fields, str),
        (float_fields, float),
        (date_fields, str)
    ]:
        type_check = check_type_values(data, fields_group, expected_type)
        if type_check:
            return type_check

        # update fields
        field_to_update = []
        for field in fields:
            if field in data:
                field_to_update.append(field)

    request_edit = modify_task(task_id, data, field_to_update, keys_ignored)
    return request_edit


@task_endpoints.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    request_remove = remove_task(task_id)
    return request_remove

########################################################################################################################

@task_endpoints.route('/<int:task_id>/users', methods=['POST'])
def assign_task_user(task_id):
    data = request.get_json()
    if not data:
        return {'error': 'Missing required fields',
                'message': 'The request body is empty or missing required fields'
                }, 400

    # check for required keys
    key_check = check_key_values(data, ['user_id'])
    if key_check:
        return key_check

    # check for keys not required, then ignored
    keys_ignored = False
    if not all(k in ['user_id', 'work_hours'] for k in data):
        keys_ignored = [k for k in data if k not in ['user_id', 'work_hours']]

    # check for type validation
    type_check = check_type_values(data, ['user_id'], expected_type=int)
    if type_check:
        return type_check
    else:
        user_id = data['user_id']

    task_work_hours = None
    if 'work_hours' in data:
        type_check = check_type_values(data, ['work_hours'], expected_type=(int, float))
        if type_check:
            return type_check
        else:
            task_work_hours = data['work_hours']

    request_post = add_task_user(task_id, user_id, task_work_hours, keys_ignored)
    return request_post

@task_endpoints.route('/<int:task_id>/users/<int:user_id>', methods=['DELETE'])
def delete_task_user(task_id, user_id):
    request_remove = remove_task_user(task_id, user_id)
    return request_remove