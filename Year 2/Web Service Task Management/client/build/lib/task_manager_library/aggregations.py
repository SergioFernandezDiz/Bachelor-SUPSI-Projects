#Group_06_Bernacchia_Fernandez\client> pipenv run python -m task_manager_library.aggregations

import requests

from .modules import *
from .user_api import get_tasks_by_user, get_user_by_id
from .task_api import get_tasks, get_users_by_task, get_task_by_id, get_project_by_task
from .project_api import get_tasks_by_project, get_users_by_project, get_project_by_id
from .http_client import get, post, put, delete, terminal_response
from typing import List
from datetime import datetime

# aggregations and statistics
def get_progress_by_tasks(tasks: List[Task]) -> float:
    if len(tasks) == 0:
        return 0
    completed = sum(1 for task in tasks if task.status == 'Completed')
    return round((completed / len(tasks)) * 100, 2)

def get_progress_by_project(project: Project) -> float:
    tasks = get_tasks_by_project(project)
    progress = get_progress_by_tasks(tasks)
    return progress

def get_total_hours_by_task(task):
    users = get_users_by_task(task)
    total = sum(u.work_hours for u in users)
    return total

def get_total_hours_by_project(project):
    tasks = get_tasks_by_project(project)
    total = 0
    for task in tasks:
        work_h = get_total_hours_by_task(task)
        total += work_h
    return total

def get_total_hours_by_user(user):
    tasks = get_tasks_by_user(user)
    total = sum(t.work_hours for t in tasks)
    return total

def get_hours_on_project_by_user(user, project):
    tasks = get_tasks_by_user(user)
    total = 0
    for task in tasks:
        p = get_project_by_task(task)
        if p.id == project.id:
            total += task.work_hours
    return total

if __name__ == '__main__':
    print("-------------------------------------------")
    tasks = get_tasks()
    result = get_progress_by_tasks(tasks)
    print(f"Progress of the all the tasks: {result}%")

    print("-------------------------------------------")
    project = get_project_by_id(1)
    result = get_progress_by_project(project)
    print(f"Progress of the project {project.id} : {result}%")

    print("-------------------------------------------")
    task = get_task_by_id(1)
    result = get_total_hours_by_task(task)
    print(f"Total working hours for task {task.id} : {result}h")

    print("-------------------------------------------")
    project = get_project_by_id(1)
    result = get_total_hours_by_project(project)
    print(f"Total working hours for project {project.id} : {result}h")

    print("-------------------------------------------")
    user = get_user_by_id(1)
    result = get_total_hours_by_user(user)
    print(f"Total working hours for user {user.id} : {result}h")

    print("-------------------------------------------")
    user = get_user_by_id(1)
    project = get_project_by_id(1)
    result = get_hours_on_project_by_user(user, project)
    print(f"Total working hours for project {project.id} by User {user.id} : {result}h")