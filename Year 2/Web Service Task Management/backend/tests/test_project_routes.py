from .conftest import test_client as client

# function to create project - to use only here
def create_project_data():
    return {
        'name': 'PROJECT 1',
        'project_type': 'Renovation',
        'project_status':  'Behind'
    }

def create_project_data_no_nullable():
    return {
        'project_type': 'Renovation',
        'project_status':  'Behind'
    }

def create_project_data_with_keys_ignored():
    return {
        'name': 'PROJECT',
        'project_type': 'Renovation',
        'project_status':  'Behind',
        'password': '<PASSWORD>'
    }

def create_project_data_with_wrong_type():
    return {
        'name': 123,
        'project_type': 123,
        'project_status': 123
    }

def create_project_data_with_invalid_type():
    return {
        'name': 'PROJECT',
        'project_type': 'INVALID',
        'project_status':  'Behind'
    }

def create_project_data_with_invalid_status():
    return {
        'name': 'PROJECT',
        'project_type': 'Renovation',
        'project_status':  'INVALID'
    }


# test GET
def test_get_projects(client):
    response = client.get('/project/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 10
    assert data[0]['name'] == 'Renovation of a School Project 001'
    assert data[1]['name'] == 'Innovation of a Classroom Project 002'

def test_get_project(client):
    response = client.get('/project/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['name'] == 'Renovation of a School Project 001'

def test_get_project_not_found(client):
    id: int = 999999
    response = client.get(f'/project/{id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {id} not found'


def test_get_project_users(client):
    id: int = 1
    response = client.get(f'/project/{id}/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['id'] == 1
    assert data[0]['username'] == '1-Bob'

    id: int = 2
    response = client.get(f'/project/{id}/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['id'] == 2
    assert data[0]['username'] == '2-Charlie'

def test_get_project_users_wrong_project(client):
    id: int = 999999
    response = client.get(f'/project/{id}/users')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {id} not found'


def test_get_project_tasks(client):
    id: int = 1
    response = client.get(f'/project/{id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Task 001 of Renovation of a School Project 001'

def test_get_project_tasks_wrong_project(client):
    id: int = 999999
    response = client.get(f'/project/{id}/tasks')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {id} not found'



# test POST
def test_create_project(client):
    # count initial total N
    N = len(client.get('/project/').get_json())

    response = client.post('/project/', json=create_project_data())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Project created successfully'

    # verify
    project_id = int(data['project']['id'])
    response = client.get(f'/project/{project_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['name'] == 'PROJECT 1'

    new_N = len(client.get('/project/').get_json())
    assert new_N == N + 1

def test_create_project_keys_ignored(client):
    # count initial total N
    N = len(client.get('/project/').get_json())

    response = client.post('/project/', json=create_project_data_with_keys_ignored())
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Project created successfully'

    # verify creation
    new_N = len(client.get('/project/').get_json())
    assert new_N == N + 1

def test_create_project_empty(client):
    # count initial total N
    N = len(client.get('/project/').get_json())

    response = client.post('/project/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get('/project/').get_json())
    assert new_N == N

def test_create_project_no_nullable(client):
    # count initial total N
    N = len(client.get('/project/').get_json())

    response = client.post('/project/', json=create_project_data_no_nullable())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get('/project/').get_json())
    assert new_N == N

def test_create_project_wrong_type(client):
    # count initial total N
    N = len(client.get('/project/').get_json())

    response = client.post('/project/', json=create_project_data_with_wrong_type())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no creation
    new_N = len(client.get('/project/').get_json())
    assert new_N == N

def test_create_project_invalid_type(client):
    # count initial total N
    N = len(client.get('/project/').get_json())

    response = client.post('/project/', json=create_project_data_with_invalid_type())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid project_type'

    # verify no creation
    new_N = len(client.get('/project/').get_json())
    assert new_N == N

def test_create_project_invalid_status(client):
    # count initial total N
    N = len(client.get('/project/').get_json())

    response = client.post('/project/', json=create_project_data_with_invalid_status())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid project_status'

    # verify no creation
    new_N = len(client.get('/project/').get_json())
    assert new_N == N



# test PUT
def test_update_project(client):
    id: int = 1
    updated = {'project_status': 'Completed'}
    response = client.put(f'/project/{id}', json=updated)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Project {id} updated successfully'

    # verify the modifications
    test_response = client.get(f'/project/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['project_status'] == 'Completed'
    assert test_data['name'] == 'Renovation of a School Project 001'

def test_update_project_empty(client):
    id: int = 1
    response = client.put(f'/project/{id}', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields' or data['warning'] == 'No valid fields provided'

    # verify the modifications
    test_response = client.get(f'/project/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['name'] == 'Renovation of a School Project 001'
    assert test_data['project_status'] == 'Behind'

def test_update_project_wrong(client):
    id: int = 999999
    updated = {'name': 'PROJECT UPDATED'}
    response = client.put(f'/project/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {id} not found'

def test_update_project_keys_ignored(client):
    id: int = 1
    updated = {'name': 'PROJECT UPDATED',
               'password': '<PASSWORD>'}
    response = client.put(f'/project/{id}', json=updated)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Project {id} updated successfully'

    # verify the modifications
    test_response = client.get(f'/project/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['name'] == 'PROJECT UPDATED'
    assert test_data['project_type'] == 'Renovation'

def test_update_project_wrong_type(client):
    id: int = 1
    updated = {'name': 123}
    response = client.put(f'/project/{id}', json=updated)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no modifications
    test_response = client.get(f'/project/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['name'] == 'Renovation of a School Project 001'
    assert test_data['project_type'] == 'Renovation'

def test_update_project_invalid_status(client):
    id: int = 1
    updated = {'project_status': 'INVALID'}
    response = client.put(f'/project/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid project_status'

    # verify no modifications
    test_response = client.get(f'/project/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['project_status'] == 'Behind'
    assert test_data['name'] == 'Renovation of a School Project 001'

def test_update_project_invalid_type(client):
    id: int = 1
    updated = {'project_type': 'INVALID'}
    response = client.put(f'/project/{id}', json=updated)
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid project_type'

    # verify no modifications
    test_response = client.get(f'/project/{id}')
    assert test_response.status_code == 200
    test_data = test_response.get_json()
    assert test_data['project_type'] == 'Renovation'
    assert test_data['name'] == 'Renovation of a School Project 001'



# test DELETE
def test_delete_project(client):
    # count total N
    N = len(client.get('/project/').get_json())

    id: int = 1
    response = client.delete(f'/project/{id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == f'Project {id} deleted successfully'

    # verify new counter : N-1
    new_N = len(client.get('/project/').get_json())
    assert new_N == N - 1

def test_delete_project_not_existing(client):
    # count total N
    N = len(client.get('/project/').get_json())

    id: int = 10000
    response = client.delete(f'/project/{id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {id} does not exist'

    # verify no removed projects
    new_N = len(client.get('/project/').get_json())
    assert new_N == N




# relationship many-to-many
# PROJECT-USER
def create_relationship_user_complete(user_id):
    return {
        'user_id': user_id,
        'role': 'Admin'
    }

def create_relationship_user_minimal(user_id):
    return {
        'user_id': user_id
    }

def create_relationship_user_no_nullable():
    return {
        'role': 'Admin'
    }

def create_relationship_user_key_ignored():
    return {
        'user_id': 1,
        'role': 'Admin',
        'nullable': True
    }

def create_relationship_user_wrong_type():
    return {
        'user_id': 'WRONG TYPE'
    }

def create_relationship_user_invalid_role():
    return {
        'user_id': 2,
        'role': 'OTHER'
    }

# test RELATIONSHIPS MANY TO MANY
def test_assign_project_user(client):
    user_id: int = 1
    project_id: int = 2

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_complete(user_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Project {project_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/project/{project_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_user_complete(user_id)
    for t in data:
        if t['id'] == expected_result['user_id']:
            assert t['role'] == expected_result['role']

    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N + 1

def test_assign_project_user_minimal(client):
    user_id: int = 1
    project_id: int = 2

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_minimal(user_id))
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == f'Project {project_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/project/{project_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_user_complete(user_id)
    expected_result['role'] = 'Normal'
    for t in data:
        if t['id'] == expected_result['user_id']:
            assert t['role'] == expected_result['role']

    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N + 1

def test_assign_project_user_update_role(client):
    user_id: int = 1
    project_id: int = 1 # existing yet

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_complete(user_id))
    assert response.status_code == 201

    # verify update
    response = client.get(f'/project/{project_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == project_id:
            update_role = t['role']
    assert update_role == create_relationship_user_complete(user_id)['role']

    # verify no creation
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N


def test_assign_project_user_no_update_role(client):
    user_id: int = 1
    project_id: int = 1  # existing yet

    # actual work_hours
    response = client.get(f'/project/{project_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == user_id:
            role = t['role']

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_minimal(user_id))
    assert response.status_code == 201

    # verify update
    response = client.get(f'/project/{project_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    for t in data:
        if t['id'] == user_id:
            update_role = t['role']
    assert update_role == role

    # verify no creation
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N


def test_assign_project_user_keys_ignored(client):
    project_id: int = 2

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_key_ignored())
    assert response.status_code == 201
    data = response.get_json()
    user_id = create_relationship_user_key_ignored()['user_id']
    assert data['message'] == f'Project {project_id} assigned to User {user_id} successfully'

    # verify creation
    response = client.get(f'/project/{project_id}/users')
    assert response.status_code == 200
    data = response.get_json()
    expected_result = create_relationship_user_key_ignored()
    for t in data:
        if t['id'] == expected_result['user_id']:
            assert t['role'] == expected_result['role']

    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N + 1

def test_assign_user_user_empty(client):
    project_id: int = 1

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N

def test_assign_project_user_no_nullable(client):
    project_id: int = 1

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_no_nullable())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing required fields'

    # verify no creation
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N


def test_assign_project_user_wrong_type(client):
    project_id: int = 1

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_wrong_type())
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid data type'

    # verify no creation
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N


def test_assign_project_user_invalid_project(client):
    project_id: int = 100000

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_complete(2))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {project_id} not found'


def test_assign_project_user_invalid_user(client):
    project_id: int = 1
    user_id: int = 100000

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_complete(user_id))
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'

    # verify no creation
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N

def test_assign_project_user_invalid_role(client):
    project_id: int = 1

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.post(f'/project/{project_id}/users', json=create_relationship_user_invalid_role())
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Invalid user_role'

    # verify no creation
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N


def test_delete_project_user(client):
    user_id: int = 1
    project_id: int = 1

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.delete(f'/project/{project_id}/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == f'User {user_id} deleted successfully from Project {project_id}'

    # verify deleting
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N - 1


def test_delete_project_user_not_existing(client):
    user_id: int = 1
    project_id: int = 2

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.delete(f'/project/{project_id}/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {project_id} is not assigned to User {user_id} yet'

    # verify no deleting
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N


def test_delete_project_user_invalid_project(client):
    user_id: int = 1
    project_id: int = 2000000

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.delete(f'/project/{project_id}/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'Project {project_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N


def test_delete_project_user_invalid_user(client):
    user_id: int = 100000
    project_id: int = 1

    # count total N
    N = len(client.get(f'/project/{project_id}/users').get_json())

    response = client.delete(f'/project/{project_id}/users/{user_id}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == f'User {user_id} not found'

    # verify no deleting
    new_N = len(client.get(f'/project/{project_id}/users').get_json())
    assert new_N == N