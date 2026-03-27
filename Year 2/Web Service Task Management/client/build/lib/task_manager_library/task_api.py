# from \client run: python -m task_manager_library.task_api

import requests
from .modules import *
from .project_api import get_project_by_id
from .http_client import get, post, put, delete, terminal_response
from typing import List


def get_tasks() -> List[Task]:
    response = get('task/').json()
    terminal_response(response)
    tasks:List[Task] = [Task.from_json(t) for t in response]
    return tasks

def list_tasks_all_status() -> List[str]:
    response = get('task/status').json()
    terminal_response(response)
    return [r['status'] for r in response]

def list_tasks_all_priorities() -> List[str]:
    response = get('task/priorities').json()
    terminal_response(response)
    return [r['level'] for r in response]

def get_task_by_id(task_id:int) -> Task:
    response = get(f'task/{task_id}').json()
    terminal_response(response)
    # substitute project_id with the project object
    project_id: int = response.pop('project_id')
    response['project_id'] = project_id

    task = Task.from_json(response)
    return task

def get_project_by_task(task:Task):
    project = get_project_by_id(task.project_id)
    return project

def get_users_by_task(task:Task) -> List[User]:
    id = task.id
    response = get(f'task/{id}/users').json()
    terminal_response(response)
    users: List[User] = [User.from_json(u) for u in response]
    return users

def create_task( task: Task ) -> Task:
    data = task.to_dict()
    response = post(f'task/', data).json()
    terminal_response(response)
    if 'task' not in response:
        raise ValueError('Error in the response')
    task = Task.from_json(response['task'])
    return task

def update_task(task: Task) -> Task:
    data = task.to_dict()
    response = put(f'task/{task.id}', json=data).json()
    terminal_response(response)
    updated_task: Task = get_task_by_id(task.id)
    return updated_task

def delete_task(task_id: int):
    response = delete(f'task/{task_id}').json()
    terminal_response(response)

if __name__ == '__main__':

    print("Print task")
    task = get_task_by_id(1)
    print(task)

    print("-------------------------------------------")
    print("Print list of tasks")
    tasks = get_tasks()
    for t in tasks[:2]:
        print(t)

    print("-------------------------------------------")
    print("Print users of a task")
    users = get_users_by_task(task)
    for u in users:
        print(u)

    print("-------------------------------------------")
    print("Creating new Task")
    proj = get_project_by_id(1)
    new_task = Task(name="TASK ADDED", location="Minusio", status="Pending", project_id=proj.id)
    c_new_task = create_task(new_task)
    print("Created Task:", c_new_task)

    print("-------------------------------------------")
    print("Task Updated")
    up_task = Task(task_id=1, name='TASK UPDATED', location="Minusio", status="Pending", project_id=proj.id)
    result = update_task(up_task)
    print("Update result:", result)

    print("-------------------------------------------")
    print("Delete Task")
    result = delete_task(10)
    print(result)

    print("-------------------------------------------")
    print('\n All status:')
    result = list_tasks_all_status()
    print(result)

    print("-------------------------------------------")
    print('\n All priorities:')
    result = list_tasks_all_priorities()
    print(result)