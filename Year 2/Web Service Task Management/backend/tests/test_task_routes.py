from datetime import datetime
from .conftest import test_client as client

# function to create Task
def create_task_data():
    return {
        "name": "Prepare Report",
        "location": "Office",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "actual_cost": 500.0,
        "budget": 1000.0,
        "project_id": 1,
        "status": "Pending",
        "priority": "High"
    }

def create_task_missing_required():
    return {
        "location": "Office",
        # Missing: name, start_date, project_id, status
    }

def create_task_invalid_types():
    return {
        "name": 123,                         # should be str
        "location": 456,                     # should be str
        "start_date": 789,                   # should be ISO 8601 str
        "project_id": "not_an_int",          # should be int
        "status": 999                        # should be str
    }

def create_task_extra_fields():
    return {
        "name": "Task With Extra",
        "location": "Overthere",
        "start_date": datetime.now().isoformat(),
        "project_id": 1,
        "status": "Pending",
        "extra_field_1": "surprise",
        "extra_field_2": 999
    }

def create_task_data_with_invalid_status():
    return {
        "name": "Prepare Report",
        "location": "Office",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "actual_cost": 500.0,
        "budget": 1000.0,
        "project_id": 1,
        "status": "INVALID",
        "priority": "High"
    }

def create_task_data_with_invalid_priority():
    return {
        "name": "Prepare Report",
        "location": "Office",
        "start_date": datetime.now().isoformat(),
        "end_date": datetime.now().isoformat(),
        "actual_cost": 500.0,
        "budget": 1000.0,
        "project_id": 1,
        "status": "Pending",
        "priority": "INVALID"
    }



# test GET
def test_get_tasks(client):
    response = client.get('/task/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 30
    assert data[0]['name'] == 'Task 001 of Renovation of a School Project 001'
    assert data[1]['name'] == 'Task 002 of Renovation of a School Project 001'

def test_get_task(client):
    response = client.get('/task/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['name'] == 'Task 001 of Renovation of a School Project 001'

def test_get_task_not_found(client):
    id: int = 999999
    response = client.get(f'/task/{id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {id} not found'


def test_get_task_users(client):
    id: int = 1
    response = client.get(f'/task/{id}/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Bob'

    id: int = 2
    response = client.get(f'/task/{id}/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == 2
    assert data[0]['name'] == 'Charlie'

def test_get_task_users_wrong_task(client):
    id: int = 999999
    response = client.get(f'/task/{id}/users')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {id} not found'



# test POST
def test_create_task(client):
    # count initial total N
    N = len(client.get('/task/').get_json())

    response = client.post('/task/', json=create_task_data())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Task created successfully'

    # verify
    user_id = int(data['task']['id'])
    response = client.get(f'/task/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['name'] == 'Prepare Report'

    new_N = len(client.get('/task/').get_json())
    assert new_N == N + 1

def test_create_task_keys_ignored(client):
    # count initial total N
    N = len(client.get('/task/').get_json())

    response = client.post('/task/', json=create_task_extra_fields())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Task created successfully'

    # verify creation
    new_N = len(client.get('/task/').get_json())
    assert new_N == N + 1

def test_create_task_empty(client):
    # count initial total N
    N = len(client.get('/task/').get_json())

    response = client.post('/task/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get('/task/').get_json())
    assert new_N == N

def test_create_task_no_nullable(client):
    # count initial total N
    N = len(client.get('/task/').get_json())

    response = client.post('/task/', json=create_task_missing_required())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get('/task/').get_json())
    assert new_N == N

def test_create_task_wrong_type(client):
    # count initial total N
    N = len(client.get('/task/').get_json())

    response = client.post('/task/', json=create_task_invalid_types())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no creation
    new_N = len(client.get('/task/').get_json())
    assert new_N == N

def test_create_task_invalid_status(client):
    # count initial total N
    N = len(client.get('/task/').get_json())

    response = client.post('/task/', json=create_task_data_with_invalid_status())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid status'

    # verify no creation
    new_N = len(client.get('/task/').get_json())
    assert new_N == N


def test_create_task_invalid_priority(client):
    # count initial total N
    N = len(client.get('/task/').get_json())

    response = client.post('/task/', json=create_task_data_with_invalid_priority())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid priority'

    # verify no creation
    new_N = len(client.get('/task/').get_json())
    assert new_N == N



# test PUT
def test_update_task(client):
    id = 1
    updated = {'status': 'Pending'}
    response = client.put(f'/task/{id}', json=updated)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Task {id} updated successfully'

    # verify the update
    get_response = client.get(f'/task/{id}')
    assert get_response.status_code == 200
    task_data = get_response.get_json()
    assert task_data['name'] == 'Task 001 of Renovation of a School Project 001'
    assert task_data['status'] == 'Pending'


def test_update_task_wrong(client):
    id: int = 999999
    updated = {'name': 'PROJECT UPDATED'}
    response = client.put(f'/project/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {id} not found'

def test_update_task_empty(client):
    id = 1
    response = client.put(f'/task/{id}', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

def test_update_task_not_found(client):
    id = 999999
    updated = {'name': 'Task'}
    response = client.put(f'/task/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {id} not found'

def test_update_task_keys_ignored(client):
    id = 1
    updated = {'name': 'New Task Name', 'unexpected_key': 'value'}
    response = client.put(f'/task/{id}', json=updated)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Task {id} updated successfully'

    # verify update, key ignored
    get_response = client.get(f'/task/{id}')
    task_data = get_response.get_json()
    assert task_data['name'] == 'New Task Name'
    assert 'unexpected_key' not in task_data

def test_update_task_wrong_type(client):
    id = 1
    updated = {'name': 12345}  # invalid type
    response = client.put(f'/task/{id}', json=updated)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no modifications
    get_response = client.get(f'/task/{id}')
    assert get_response.status_code == 200
    task_data = get_response.get_json()
    assert task_data['name'] == 'Task 001 of Renovation of a School Project 001'

def test_update_task_invalid_status(client):
    id: int = 1
    updated = {'status': 'INVALID'}
    response = client.put(f'/task/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid status'

    # verify no modifications
    get_response = client.get(f'/task/{id}')
    assert get_response.status_code == 200
    task_data = get_response.get_json()
    assert task_data['name'] == 'Task 001 of Renovation of a School Project 001'
    assert task_data['status'] == 'In Progress'

def test_update_task_invalid_priority(client):
    id: int = 1
    updated = {'priority': 'INVALID'}
    response = client.put(f'/task/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid priority'

    # verify no modifications
    get_response = client.get(f'/task/{id}')
    assert get_response.status_code == 200
    task_data = get_response.get_json()
    assert task_data['name'] == 'Task 001 of Renovation of a School Project 001'
    assert task_data['priority'] == 'Medium'



# test DELETE
def test_delete_task(client):
    # count total N
    N = len(client.get('/task/').get_json())

    id: int = 1
    response = client.delete(f'/task/{id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == f'Task {id} deleted successfully'

    # verify new counter : N-1
    new_N = len(client.get('/task/').get_json())
    assert new_N == N - 1


def test_delete_user_not_existing(client):
    # count total N
    N = len(client.get('/task/').get_json())

    id: int = 10000
    response = client.delete(f'/task/{id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {id} does not exist'

    # verify no removed users
    new_N = len(client.get('/task/').get_json())
    assert new_N == N


# relationship many-to-many
# TASK-USER
def create_relationship_user_complete(user_id):
    return {
        'user_id': user_id,
        'work_hours': 10
    }

def create_relationship_user_minimal(user_id):
    return {
        'user_id': user_id
    }

def create_relationship_user_no_nullable():
    return {
        'work_hours': 10.0
    }

def create_relationship_user_key_ignored():
    return {
        'user_id': 2,
        'work_hours': 10.0,
        'nullable': True
    }

def create_relationship_user_wrong_type():
    return {
        'user_id': 'WRONG TYPE'
    }

def create_relationship_user_invalid_work_hours():
    return {
        'user_id': 2,
        'work_hours': -10.0
    }

# test RELATIONSHIPS MANY TO MANY
def test_assign_task_user(client):
    user_id: int = 1
    task_id: int = 2

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_complete(user_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Task {task_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/task/{task_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    user_added = False
    for t in data:
        if t['id'] == user_id:
            user_added = True
    assert user_added == True

    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N + 1

def test_assign_task_user_minimal(client):
    user_id: int = 2
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_minimal(user_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Task {task_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/task/{task_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    user_added = False
    for t in data:
        if t['id'] == user_id:
            user_added = True
    assert user_added == True

    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N + 1


def test_assign_task_user_update_work_hours(client):
    user_id: int = 1
    task_id: int = 1 # existing yet

    # actual work_hours - using user endpoint
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            work_hours = t['work_hours']

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_complete(user_id))
    assert response.status_code == 201

    # verify update - using user endpoint
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            update_work_hours = t['work_hours']
    assert update_work_hours == work_hours + create_relationship_user_complete(user_id)['work_hours']

    # verify no creation
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_assign_task_user_no_update_work_hours(client):
    user_id: int = 1
    task_id: int = 1  # existing yet

    # actual work_hours - using user endpoint
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            work_hours = t['work_hours']

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_minimal(user_id))
    assert response.status_code == 201

    # verify update - using user endpoint
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            update_work_hours = t['work_hours']
    assert update_work_hours == work_hours

    # verify no creation
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_assign_task_user_keys_ignored(client):
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_key_ignored())
    assert response.status_code == 201
    data = response.get_json()
    user_id = create_relationship_user_key_ignored()['user_id']
    assert data['message'] == f'Task {task_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/task/{task_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    user_added = False
    for t in data:
        if t['id'] == user_id:
            user_added = True
    assert user_added == True

    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N + 1


def test_assign_task_user_empty(client):
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_assign_task_user_no_nullable(client):
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_no_nullable())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_assign_task_user_wrong_type(client):
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_wrong_type())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no creation
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_assign_task_user_invalid_task(client):
    task_id: int = 100000

    response = client.post(f'/task/{task_id}/tasks', json=create_relationship_user_complete(2))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {task_id} not found'


def test_assign_task_user_invalid_task(client):
    task_id: int = 1
    user_id: int = 100000

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_complete(user_id))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'

    # verify no creation
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N

def test_assign_task_user_invalid_work_hours(client):
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.post(f'/task/{task_id}/users', json=create_relationship_user_invalid_work_hours())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid work_hours'

    # verify no creation
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_delete_task_user(client):
    user_id: int = 1
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.delete(f'/task/{task_id}/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == f'User {user_id} deleted successfully from Task {task_id}'

    # verify deleting
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N - 1


def test_delete_task_user_not_existing(client):
    user_id: int = 1
    task_id: int = 2

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.delete(f'/task/{task_id}/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {task_id} is not assigned to User {user_id} yet'

    # verify no deleting
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_delete_task_user_invalid_task(client):
    user_id: int = 1
    task_id: int = 2000000

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.delete(f'/task/{task_id}/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {task_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N


def test_delete_task_user_invalid_user(client):
    user_id: int = 100000
    task_id: int = 1

    # count total N
    N = len(client.get(f'/task/{task_id}/users').get_json())

    response = client.delete(f'/task/{task_id}/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/task/{task_id}/users').get_json())
    assert new_N == N