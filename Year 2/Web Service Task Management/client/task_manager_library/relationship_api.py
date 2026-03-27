# from \client run: python -m task_manager_library.relationship_api

from .project_api import get_project_by_id
from .task_api import get_task_by_id
from .user_api import get_user_by_id
from .modules import *
from .http_client import get, post, put, delete, terminal_response

# UserProjects
def assign_user_to_project(user: User, project: Project, role:str = None):
    data = {'project_id': project.id, 'role': role }
    response = post(f'user/{user.id}/projects', json=data)
    terminal_response(response)

def remove_user_from_project(user: User, project: Project):
    response = delete(f'user/{user.id}/projects/{project.id}')
    terminal_response(response)

def assign_project_to_user( project: Project, user: User, role:str = None):
    data = {'user_id': user.id, 'role': role}
    response = post(f'project/{project.id}/users', json=data)
    terminal_response(response)

def remove_project_from_user( project: Project, user: User):
    response = delete(f'project/{project.id}/users/{user.id}')
    terminal_response(response)

# UserTasks
def assign_user_to_task(user: User, task: Task, work_hours:float = None):
    data = {'task_id': task.id, 'work_hours': work_hours }
    response = post(f'user/{user.id}/tasks', json=data)
    terminal_response(response)

def remove_user_from_task( task: Task, user: User):
    response = delete(f'user/{user.id}/tasks/{task.id}')
    terminal_response(response)

def assign_task_to_user( task: Task, user: User, work_hours:float = None):
    data = {'user_id': user.id, 'work_hours': work_hours}
    response = post(f'task/{task.id}/users', json=data)
    terminal_response(response)

def remove_task_from_user( task: Task, user: User):
    response = delete(f'user/{user.id}/tasks/{task.id}')
    terminal_response(response)

if __name__ == '__main__':

    project = get_project_by_id(10)
    task = get_task_by_id(100)
    user = get_user_by_id(7)

    print("-------------------------------------------")
    print("Assignment USER - PROJECT")
    assign_user_to_project(user, project)
    assign_project_to_user(project, user)

    print("-------------------------------------------")
    print("Assignment USER - TASK")
    assign_task_to_user(task, user)
    assign_user_to_task(user, task)