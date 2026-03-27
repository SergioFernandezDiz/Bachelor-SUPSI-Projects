# from \client run: python -m task_manager_library.project_api

from .modules import *
from .http_client import get, post, put, delete, terminal_response
from typing import List


def get_projects() -> List[Project]:
    response = get('project/').json()
    terminal_response(response)
    projects: List[Project] = [Project.from_json(p) for p in response]
    return projects

def list_projects_all_status() -> List[str]:
    response = get('project/status').json()
    terminal_response(response)
    return [r['status'] for r in response]

def list_projects_all_types() -> List[str]:
    response = get('project/types').json()
    terminal_response(response)
    return [r['type'] for r in response]

def get_project_by_id(project_id:int) -> Project:
    response = get(f'project/{project_id}').json()
    terminal_response(response)
    project: Project = Project.from_json(response)
    return project

def get_users_by_project(project:Project) -> List[User]:
    id = project.id
    response = get(f'project/{id}/users').json()
    terminal_response(response)
    users: List[User] = [User.from_json(u) for u in response]
    return users

def get_tasks_by_project(project:Project) -> List[Task]:
    id = project.id
    response = get(f'project/{id}/tasks').json()
    terminal_response(response)
    tasks: List[Task] = [Task.from_json(t) for t in response]
    return tasks

def create_project(project: Project) -> Project:
    data: dict = project.to_dict()
    response = post(f'project/', data).json()
    terminal_response(response)
    if 'project' not in response:
        raise ValueError('Error in the response')
    project: Project = Project.from_json(response['project'])
    return project

def update_project(project: Project) -> Project:
    data: dict = project.to_dict()
    project_id = data.pop('id')
    response = put(f'project/{project_id}', data).json()
    terminal_response(response)
    updated_project: Project = get_project_by_id(project_id)
    return updated_project

def delete_project(project_id: int):
    response = delete(f'project/{project_id}').json()
    terminal_response(response)



if __name__ == '__main__':

    print("Print project")
    project = get_project_by_id(1)
    print(project)

    print("-------------------------------------------")
    print("Print list projects")
    projects= get_projects()
    for p in projects[:2]:
        print(p)

    print("-------------------------------------------")
    print("Print users of a project")
    users = get_users_by_project(project)
    for u in users:
        print(u)

    print("-------------------------------------------")
    print("Print tasks of a project")
    tasks = get_tasks_by_project(project)
    for t in tasks:
        print(t)

    print("-------------------------------------------")
    print("Creating new project")
    project = Project(name="NEW PROJECT", project_type="Other", project_status="On Hold")
    new_project = create_project(project)
    print("Created project:", new_project)

    print("-------------------------------------------")
    print("Updating project")
    up_project = Project(project_id=1, name='PROJECT UPDATED', project_type="Other")
    print(up_project)
    result = update_project(up_project)
    print("Update result:", result)

    print("-------------------------------------------")
    print("Deleting project")
    result = delete_project(project_id=3)
    print("Delete result:", result)

    print('\n All status:')
    result = list_projects_all_status()
    print(result)

    print('\n All types:')
    result = list_projects_all_types()
    print(result)