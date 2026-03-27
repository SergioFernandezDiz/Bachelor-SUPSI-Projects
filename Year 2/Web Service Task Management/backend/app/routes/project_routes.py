from flask import request,Blueprint
from routes._utils import check_type_values, check_key_values
from routes.project_service import *

project_endpoints = Blueprint('project_endpoints',__name__, url_prefix='/project')

fields = ['name', 'project_type', 'project_status']
key_fields = ['name', 'project_type', 'project_status']
str_fields = ['name', 'project_type', 'project_status']

@project_endpoints.route('/', methods=['GET'])
def get_projects():
    projects = get_all_projects()
    return projects

@project_endpoints.route('/status', methods=['GET'])
def get_tasks_status():
    status = get_all_status()
    return status

@project_endpoints.route('/types', methods=['GET'])
def get_tasks_priorities():
    types = get_all_types()
    return types


@project_endpoints.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = get_specific_project(project_id)
    return project

@project_endpoints.route('/<int:project_id>/users', methods=['GET'])
def get_project_users(project_id):
    request_projectusers = get_specific_project_users(project_id)
    return request_projectusers

@project_endpoints.route('/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    request_projecttasks = get_specific_project_tasks(project_id)
    return request_projecttasks

##############################################################################

@project_endpoints.route('/', methods=['POST'])
def create_project():
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
    keys_ignored = None
    if not all(k in fields for k in data):
        keys_ignored = [k for k in data if k not in fields]

    request_creation = add_project(data, keys_ignored)
    return request_creation

##############################################################################

@project_endpoints.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
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

    request_edit = modify_project(project_id, data, field_to_update, keys_ignored)
    return request_edit

##############################################################################

@project_endpoints.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    request_remove = remove_project(project_id)
    return request_remove

########################################################################################################################

@project_endpoints.route('/<int:project_id>/users', methods=['POST'])
def assign_project_user(project_id):
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
    if not all(k in ['user_id', 'role'] for k in data):
        keys_ignored = [k for k in data if k not in ['user_id', 'role']]

    # check for type validation
    type_check = check_type_values(data, ['user_id'], expected_type=int)
    if type_check:
        return type_check
    else:
        user_id = data['user_id']

    user_role = None
    if 'role' in data:
        type_check = check_type_values(data, ['role'], expected_type=str)
        if type_check:
            return type_check
        else:
            user_role = data['role']

    request_post = add_project_user(project_id, user_id, user_role, keys_ignored)
    return request_post

@project_endpoints.route('/<int:project_id>/users/<int:user_id>', methods=['DELETE'])
def delete_project_user(project_id, user_id):
    request_remove = remove_project_user(project_id, user_id)
    return request_remove