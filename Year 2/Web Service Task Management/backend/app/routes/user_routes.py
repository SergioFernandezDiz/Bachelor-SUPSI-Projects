from flask import request, Blueprint,jsonify
from models import *
from routes._utils import check_type_values, check_key_values
from routes.user_service import get_all_users, get_specific_user, get_specific_user_tasks, get_specific_user_projects, add_user, modify_user, remove_user, add_user_project, remove_user_project, add_user_task, remove_user_task

users_bp = Blueprint('user', __name__, url_prefix='/user')
fields = ['username', 'name', 'last_name']
key_fields = ['username', 'name', 'last_name']
str_fields = ['username', 'name', 'last_name']
@users_bp.route('/', methods=['GET'])
def get_users():
    users = get_all_users()
    return users

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    request_user = get_specific_user(user_id)
    return request_user

@users_bp.route('/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    request_usertasks = get_specific_user_tasks(user_id)
    return request_usertasks

@users_bp.route('/<int:user_id>/projects', methods=['GET'])
def get_user_projects(user_id):
    request_userprojects = get_specific_user_projects(user_id)
    return request_userprojects

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()

    # check for required keys
    key_check = check_key_values(data, key_fields)
    if key_check:
        return key_check

    # check for type validation
    type_check = check_type_values(data, str_fields, expected_type=str)
    if type_check:
        return type_check

    # check for keys not required, then ignored
    keys_ignored = False
    if not all(k in fields for k in data):
        keys_ignored = [k for k in data if k not in fields]

    new_user = User(
        username=data['username'],
        name=data['name'],
        last_name=data['last_name'])

    request_creation = add_user(new_user, keys_ignored)
    return request_creation

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return {'error': 'Missing required fields',
                'message': 'The request body is empty or missing required fields'
                }, 400

    # check for keys not required, then ignored
    keys_ignored = False
    if not all(k in fields for k in data):
        keys_ignored = [k for k in data if k not in fields]

    # check for type validation
    type_check = check_type_values(data, str_fields, expected_type=str)
    if type_check:
        return type_check

    # update fields
    field_to_update = []
    for field in fields:
        if field in data:
            field_to_update.append(field)

    request_edit = modify_user(user_id, data, field_to_update, keys_ignored)
    return request_edit

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    request_remove = remove_user(user_id)
    return request_remove

########################################################################################################################

@users_bp.route('/<int:user_id>/projects', methods=['POST'])
def assign_user_project(user_id):
    data = request.get_json()
    if not data:
        return {'error': 'Missing required fields',
                'message': 'The request body is empty or missing required fields'
                }, 400

    # check for required keys
    key_check = check_key_values(data, ['project_id'])
    if key_check:
        return key_check

    # check for keys not required, then ignored
    keys_ignored = False
    if not all(k in ['project_id', 'role'] for k in data):
        keys_ignored = [k for k in data if k not in ['project_id', 'role']]

    # check for type validation
    type_check = check_type_values(data, ['project_id'], expected_type=int)
    if type_check:
        return type_check
    else:
        project_id = data['project_id']

    user_role = None
    if 'role' in data:
        type_check = check_type_values(data, ['role'], expected_type=str)
        if type_check:
            return type_check
        else:
            user_role = data['role']

    request_post = add_user_project(project_id, user_id, user_role, keys_ignored)
    return request_post

@users_bp.route('/<int:user_id>/projects/<int:project_id>', methods=['DELETE'])
def delete_user_project(user_id, project_id):
    request_remove = remove_user_project(project_id, user_id)
    return request_remove

########################################################################################################################

@users_bp.route('/<int:user_id>/tasks', methods=['POST'])
def assign_user_task(user_id):
    data = request.get_json()
    if not data:
        return {'error': 'Missing required fields',
                'message': 'The request body is empty or missing required fields'
                }, 400

    # check for required keys
    key_check = check_key_values(data, ['task_id'])
    if key_check:
        return key_check

    # check for keys not required, then ignored
    keys_ignored = False
    if not all(k in ['task_id', 'work_hours'] for k in data):
        keys_ignored = [k for k in data if k not in ['task_id', 'work_hours']]

    # check for type validation
    type_check = check_type_values(data, ['task_id'], expected_type=int)
    if type_check:
        return type_check
    else:
        task_id = data['task_id']

    task_work_hours = None
    if 'work_hours' in data:
        type_check = check_type_values(data, ['work_hours'], expected_type=(int, float))
        if type_check:
            return type_check
        else:
            task_work_hours = data['work_hours']

    request_post = add_user_task(task_id, user_id, task_work_hours, keys_ignored)
    return request_post

@users_bp.route('/<int:user_id>/tasks/<int:task_id>', methods=['DELETE'])
def delete_user_task(user_id, task_id):
    request_remove = remove_user_task(task_id, user_id)
    return request_remove