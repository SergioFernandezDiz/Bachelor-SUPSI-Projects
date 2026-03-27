from .conftest import test_client as client

# function to create user - to use only here
def create_user_data():
    return {
        'username': 'mr',
        'name': 'Marco',
        'last_name': 'Rossi'
    }

def create_user_data2():
    return {
        'username': 'lb',
        'name': 'Luca',
        'last_name': 'Bianchi'
    }

def create_user_data_no_nullable():
    return {
        'name': 'Marco'
    }

def create_user_data_with_keys_ignored():
    return {
        'username': 'mr',
        'name': 'Marco',
        'last_name': 'Rossi',
        'password': '<PASSWORD>'
    }

def create_user_data_with_wrong_type():
    return {
        'username': 123,
        'name': 123,
        'last_name': 123
    }



# test GET
def test_get_users(client):
    response = client.get('/user/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 6
    assert data[0]['username'] == '1-Bob'
    assert data[1]['username'] == '2-Charlie'

def test_get_user(client):
    response = client.get('/user/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['username'] == '1-Bob'

def test_get_user_not_found(client):
    id: int = 999999
    response = client.get(f'/user/{id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {id} not found'


def test_get_user_tasks(client):
    id: int = 1
    response = client.get(f'/user/{id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Task 001 of Renovation of a School Project 001'
    assert data[0]['work_hours'] == 12.0

    id: int = 2
    response = client.get(f'/user/{id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 13
    assert data[0]['id'] == 2
    assert data[0]['name'] == 'Task 002 of Renovation of a School Project 001'
    assert data[0]['work_hours'] == 4.0

def test_get_user_tasks_wrong_user(client):
    id: int = 999999
    response = client.get(f'/user/{id}/tasks')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {id} not found'


def test_get_user_projects(client):
    id: int = 1
    response = client.get(f'/user/{id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Renovation of a School Project 001'

    id: int = 2
    response = client.get(f'/user/{id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 8
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Renovation of a School Project 001'

def test_get_user_projects_wrong_user(client):
    id: int = 999999
    response = client.get(f'/user/{id}/projects')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {id} not found'



# test POST
def test_create_user(client):
    # count initial total N
    N = len(client.get('/user/').get_json())

    response = client.post('/user/', json=create_user_data())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'

    # verify
    user_id = int(data['user']['id'])
    response = client.get(f'/user/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['username'] == 'mr'

    new_N = len(client.get('/user/').get_json())
    assert new_N == N + 1

def test_create_user_keys_ignored(client):
    # count initial total N
    N = len(client.get('/user/').get_json())

    response = client.post('/user/', json=create_user_data_with_keys_ignored())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'

    # verify creation
    new_N = len(client.get('/user/').get_json())
    assert new_N == N + 1


def test_create_user_integrity_error(client):
    # add user to create UNIQUE error
    response0 = client.post('/user/', json=create_user_data())
    assert response0.status_code == 201
    # count initial total N
    N = len(client.get('/user/').get_json())

    response = client.post('/user/', json=create_user_data())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Database integrity error'

    # verify no creation
    new_N = len(client.get('/user/').get_json())
    assert new_N == N

def test_create_user_empty(client):
    # count initial total N
    N = len(client.get('/user/').get_json())

    response = client.post('/user/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get('/user/').get_json())
    assert new_N == N

def test_create_user_no_nullable(client):
    # count initial total N
    N = len(client.get('/user/').get_json())

    response = client.post('/user/', json=create_user_data_no_nullable())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get('/user/').get_json())
    assert new_N == N

def test_create_user_wrong_type(client):
    # count initial total N
    N = len(client.get('/user/').get_json())

    response = client.post('/user/', json=create_user_data_with_wrong_type())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no creation
    new_N = len(client.get('/user/').get_json())
    assert new_N == N



# test PUT
def test_update_user(client):
    id: int = 1
    updated = {'name': 'Johnny'}
    response = client.put(f'/user/{id}', json=updated)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'User {id} updated successfully'

    # verify the modifications
    test_response = client.get(f'/user/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['username'] == '1-Bob'
    assert test_data['name'] == 'Johnny'

def test_update_user_integrity_error(client):
    id: int = 2
    updated = {'username': '1-Bob'}
    response = client.put(f'/user/{id}', json=updated)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Database integrity error'

    # verify the modifications
    test_response = client.get(f'/user/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['username'] == '2-Charlie'
    assert test_data['name'] == 'Charlie'

def test_update_user_empty(client):
    id: int = 1
    response = client.put(f'/user/{id}', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify the modifications
    test_response = client.get(f'/user/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['username'] == '1-Bob'
    assert test_data['name'] == 'Bob'

def test_update_user_wrong(client):
    id: int = 999999
    updated = {'name': 'Johnny'}
    response = client.put(f'/user/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {id} not found'

def test_update_user_keys_ignored(client):
    id: int = 1
    updated = {'name': 'Johnny',
               'password': '<PASSWORD>'}
    response = client.put(f'/user/{id}', json=updated)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'User {id} updated successfully'

    # verify the modifications
    test_response = client.get(f'/user/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['username'] == '1-Bob'
    assert test_data['name'] == 'Johnny'

def test_update_user_wrong_type(client):
    id: int = 1
    updated = {'name': 123}
    response = client.put(f'/user/{id}', json=updated)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify the modifications
    test_response = client.get(f'/user/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['username'] == '1-Bob'
    assert test_data['name'] == 'Bob'



# test DELETE
def test_delete_user(client):
    # count total N
    N = len(client.get('/user/').get_json())

    id: int = 1
    response = client.delete(f'/user/{id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == f'User {id} deleted successfully'

    # verify new counter : N-1
    new_N = len(client.get('/user/').get_json())
    assert new_N == N - 1


def test_delete_user_not_existing(client):
    # count total N
    N = len(client.get('/user/').get_json())

    id: int = 10000
    response = client.delete(f'/user/{id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {id} does not exist'

    # verify no removed users
    new_N = len(client.get('/user/').get_json())
    assert new_N == N


# relationship many-to-many
# USER-TASK
def create_relationship_task_complete(task_id):
    return {
        'task_id': task_id,
        'work_hours': 10
    }

def create_relationship_task_minimal(task_id):
    return {
        'task_id': task_id
    }

def create_relationship_task_no_nullable():
    return {
        'work_hours': 10.0
    }

def create_relationship_task_key_ignored():
    return {
        'task_id': 2,
        'work_hours': 10.0,
        'nullable': True
    }

def create_relationship_task_wrong_type():
    return {
        'task_id': 'WRONG TYPE'
    }

def create_relationship_task_invalid_work_hours():
    return {
        'task_id': 2,
        'work_hours': -10.0
    }

# test RELATIONSHIPS MANY TO MANY
def test_assign_user_task(client):
    user_id: int = 1
    task_id: int = 2

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_complete(task_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Task {task_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_task_complete(task_id)
    for t in data:
        if t['id'] == expected_result['task_id']:
            assert t['work_hours'] == expected_result['work_hours']

    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N + 1

def test_assign_user_task_minimal(client):
    user_id: int = 1
    task_id: int = 2

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_minimal(task_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Task {task_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_task_complete(task_id)
    expected_result['work_hours'] = 0
    for t in data:
        if t['id'] == expected_result['task_id']:
            assert t['work_hours'] == expected_result['work_hours']

    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N + 1

def test_assign_user_task_update_work_hours(client):
    user_id: int = 1
    task_id: int = 1 # existing yet

    # actual work_hours
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            work_hours = t['work_hours']

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_complete(task_id))
    assert response.status_code == 201

    # verify update
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            update_work_hours = t['work_hours']
    assert update_work_hours == work_hours + create_relationship_task_complete(task_id)['work_hours']

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N


def test_assign_user_task_no_update_work_hours(client):
    user_id: int = 1
    task_id: int = 1  # existing yet

    # actual work_hours
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            work_hours = t['work_hours']

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_minimal(task_id))
    assert response.status_code == 201

    # verify update
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == task_id:
            update_work_hours = t['work_hours']
    assert update_work_hours == work_hours

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N


def test_assign_user_task_keys_ignored(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_key_ignored())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Task 2 assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/user/{user_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_task_key_ignored()
    for t in data:
        if t['id'] == expected_result['task_id']:
            assert t['work_hours'] == expected_result['work_hours']

    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N + 1

def test_assign_user_task_empty(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N

def test_assign_user_task_no_nullable(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_no_nullable())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N


def test_assign_user_task_wrong_type(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_wrong_type())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N


def test_assign_user_task_invalid_user(client):
    user_id: int = 100000

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_complete(2))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'


def test_assign_user_task_invalid_task(client):
    user_id: int = 1
    task_id: int = 100000

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_complete(task_id))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {task_id} not found'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N

def test_assign_user_task_invalid_work_hours(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.post(f'/user/{user_id}/tasks', json=create_relationship_task_invalid_work_hours())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid work_hours'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N


def test_delete_user_task(client):
    user_id: int = 1
    task_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.delete(f'/user/{user_id}/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == f'User {user_id} deleted successfully from Task {task_id}'

    # verify deleting
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N - 1


def test_delete_user_task_not_existing(client):
    user_id: int = 1
    task_id: int = 2

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.delete(f'/user/{user_id}/tasks/{task_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {task_id} is not assigned to User {user_id} yet'

    # verify no deleting
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N


def test_delete_user_task_invalid_task(client):
    user_id: int = 1
    task_id: int = 2000000

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.delete(f'/user/{user_id}/tasks/{task_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Task {task_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N


def test_delete_user_task_invalid_user(client):
    user_id: int = 100000
    task_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/tasks').get_json())

    response = client.delete(f'/user/{user_id}/tasks/{task_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/user/{user_id}/tasks').get_json())
    assert new_N == N



# USER-PROJECT
def create_relationship_project_complete(project_id):
    return {
        'project_id': project_id,
        'role': 'Admin'
    }

def create_relationship_project_minimal(project_id):
    return {
        'project_id': project_id
    }

def create_relationship_project_no_nullable():
    return {
        'role': 'Admin'
    }

def create_relationship_project_key_ignored():
    return {
        'project_id': 2,
        'role': 'Admin',
        'nullable': True
    }

def create_relationship_project_wrong_type():
    return {
        'project_id': 'WRONG TYPE'
    }

def create_relationship_project_invalid_role():
    return {
        'project_id': 2,
        'role': 'OTHER'
    }

# test RELATIONSHIPS MANY TO MANY
def test_assign_user_project(client):
    user_id: int = 1
    project_id: int = 2

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_complete(project_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Project {project_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/user/{user_id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_project_complete(project_id)
    for t in data:
        if t['id'] == expected_result['project_id']:
            assert t['role'] == expected_result['role']

    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N + 1

def test_assign_user_project_minimal(client):
    user_id: int = 1
    project_id: int = 2

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_minimal(project_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Project {project_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/user/{user_id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_project_complete(project_id)
    expected_result['role'] = 'Normal'
    for t in data:
        if t['id'] == expected_result['project_id']:
            assert t['role'] == expected_result['role']

    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N + 1

def test_assign_user_project_update_role(client):
    user_id: int = 1
    project_id: int = 1 # existing yet

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_complete(project_id))
    assert response.status_code == 201

    # verify update
    response = client.get(f'/user/{user_id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == project_id:
            update_role = t['role']
    assert update_role == create_relationship_project_complete(project_id)['role']

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N


def test_assign_user_project_no_update_role(client):
    user_id: int = 1
    project_id: int = 1  # existing yet

    # actual work_hours
    response = client.get(f'/user/{user_id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == project_id:
            role = t['role']

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_minimal(project_id))
    assert response.status_code == 201

    # verify update
    response = client.get(f'/user/{user_id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == project_id:
            update_role = t['role']
    assert update_role == role

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N


def test_assign_user_project_keys_ignored(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_key_ignored())
    assert response.status_code == 201
    data = response.get_json()
    project_id = create_relationship_project_key_ignored()['project_id']
    assert data['message'] == f'Project {project_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/user/{user_id}/projects')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_project_key_ignored()
    for t in data:
        if t['id'] == expected_result['project_id']:
            assert t['role'] == expected_result['role']

    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N + 1

def test_assign_user_project_empty(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N

def test_assign_user_project_no_nullable(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_no_nullable())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N


def test_assign_user_project_wrong_type(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_wrong_type())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N


def test_assign_user_project_invalid_user(client):
    user_id: int = 100000

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_complete(2))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'


def test_assign_user_project_invalid_project(client):
    user_id: int = 1
    project_id: int = 100000

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_complete(project_id))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {project_id} not found'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N

def test_assign_user_project_invalid_role(client):
    user_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.post(f'/user/{user_id}/projects', json=create_relationship_project_invalid_role())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid user_role'

    # verify no creation
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N


def test_delete_user_project(client):
    user_id: int = 1
    project_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.delete(f'/user/{user_id}/projects/{project_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == f'User {user_id} deleted successfully from Project {project_id}'

    # verify deleting
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N - 1


def test_delete_user_project_not_existing(client):
    user_id: int = 1
    project_id: int = 2

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.delete(f'/user/{user_id}/projects/{project_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {project_id} is not assigned to User {user_id} yet'

    # verify no deleting
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N


def test_delete_user_project_invalid_task(client):
    user_id: int = 1
    project_id: int = 2000000

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.delete(f'/user/{user_id}/projects/{project_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {project_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N


def test_delete_user_project_invalid_user(client):
    user_id: int = 100000
    project_id: int = 1

    # count total N
    N = len(client.get(f'/user/{user_id}/projects').get_json())

    response = client.delete(f'/user/{user_id}/projects/{project_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/user/{user_id}/projects').get_json())
    assert new_N == N