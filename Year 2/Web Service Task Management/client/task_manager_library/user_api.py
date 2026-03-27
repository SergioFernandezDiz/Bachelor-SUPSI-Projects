# from \client run: python -m task_manager_library.user_api

from .modules import *
from .http_client import get, post, put, delete, terminal_response
from typing import List



def get_users():
    response = get('user/').json()
    users:List[User] = [User.from_json(u) for u in response]
    return users

def get_user_by_id(user_id:int):
    response = get(f'user/{user_id}').json()
    user = User.from_json(response)
    return user

def get_tasks_by_user(user:User) -> List[Task]:
    id = user.id
    response = get(f'user/{id}/tasks').json()
    tasks:List[Task] = [Task.from_json(t) for t in response]
    return tasks

def get_project_by_user(user:User) -> List[Project]:
    id = user.id
    response = get(f'user/{id}/projects').json()
    projects:List[Project] = [Project.from_json(p) for p in response]
    return projects

def create_user(user: User) -> User:
    data = user.to_dict()
    response = post('user/', json=data).json()
    terminal_response(response)
    if 'user' not in response:
        raise ValueError('Error in the response')
    user = User.from_json(response['user'])
    return user

def update_user(user: User) -> User:
    data = user.to_dict()
    response = put(f'user/{user.id}', json=data).json()
    terminal_response(response)
    updated_user: User = get_user_by_id(user.id)
    return updated_user

def delete_user(user_id: int) -> dict:
    response = delete(f'user/{user_id}').json()
    terminal_response(response)



if __name__ == '__main__':
    print("Print user")
    user = get_user_by_id(1)
    print(user)

    print("-------------------------------------------")
    print("Print list users")
    users= get_users()
    for u in users[:2]:
        print(u)

    print("-------------------------------------------")
    print("Print tasks of a user")
    tasks = get_tasks_by_user(user)
    for t in tasks[:2]:
        print(t)

    print("-------------------------------------------")
    print("Print project of a user")
    projects = get_project_by_user(user)
    for p in projects[:2]:
        print(p)

    print("-------------------------------------------")
    print("Creating new user")
    new_user = User(username='MR', name='Mario', last_name='Rossi')
    c_new_user = create_user(new_user)
    print("User created:", c_new_user)

    print("-------------------------------------------")
    print("Updating user")
    new_user = User(user_id=1, username='UPDATED USERNAME', name='Mario', last_name='Rossi')
    result = update_user(new_user)
    print("Update result:", result)

    print("-------------------------------------------")
    print("Deleting user")
    result = delete_user(user_id=2)
    print("Delete result:", result)

