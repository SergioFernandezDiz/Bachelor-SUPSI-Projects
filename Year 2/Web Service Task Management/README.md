>Bernacchia Alessia, Sergio Fernandez Diz
# Group_06_Bernacchia_Fernandez

[link to the Project Report](./docs/Report.md)

## Project Overview
This repository provide a web service dedicated to task management, inspired by tools such as _Trello_ and _GitLab_. The motivation stems from the increasing need for ***coordination and clarity in project workflows***, especially within teams. The project demonstrates a functional and user-friendly API with statistical insights, offering a foundational solution to distributed task tracking and management. The resulting architecture promotes __modularity, testability, and ease of use__, and provides a solid starting point for further development in real-world collaborative contexts.

## Third-Party Code and Resources
This project uses the following third-party libraries and resources:
1. data storage &nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp;&nbsp;[__SQLite database__](https://sqlite.org/)
2. backend &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp; [__Flask app with CRUD endpoints__](https://flask.palletsprojects.com/)
3. REST API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp;__object-oriented Python client__
4. distribution&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp;[__`wheel` library permitting the usage of the api__](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)

5. tests&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp;[__`pytest` framework__](https://docs.pytest.org/)

## Folder and File Structure
The project directory is structured as follows:
```
/task_manager/
├── backend/
│   ├── app/
│   │   ├── models/                         # creates the models' tables
|   |   |   ├── __init__.py                 # manage functions' exportation
|   |   |   ├── base.py                     # create base model and initialize SQLAlchemy
|   |   |   ├── priority.py                 # priority level (used for task) model
|   |   |   ├── status.py                   # status (one for project and one for task) models
|   |   |   ├── type.py                     # type (actually only one of the project) model
|   |   |   ├── role.py                     # role (of a user in a project) model
|   |   |   ├── relationships.py            # entities relationships (usertasks and userprojects) models
|   |   |   ├── project.py                  # entity project model
|   |   |   ├── task.py                     # entity task model
|   |   |   └── user.py                     # entity user model
|   |   |
│   │   ├── routes/                         # makes the HTTP requests
|   |   |   ├── __init__.py                 # manage functions' exportation
|   |   |   ├── _utils.py                   # functions used in all modules
|   |   |   ├── _relationships_service.py   # functions used in all modules
|   |   |   ├── project_routes.py           # endpoints related to project model
|   |   |   ├── project_service.py          # database logic access layer related to project
|   |   |   ├── task_routes.py              # endpoints related to task model
|   |   |   ├── task_service.py             # database logic access layer related to task
|   |   |   ├── user_routes.py              # endpoints related to user model
|   |   |   └── user_service.py             # database logic access layer related to user
|   |   |
│   │   ├── __init__.py             
│   │   ├── _johndatabase.py                # insert initial data (from john's database)
│   │   └── app.py                          # initialize Flask app
|   |
│   ├── tests/
|   |   ├── __init__.py
|   |   ├── test_task_routes.py             # interaction tests related to tasks' endpoints
|   |   ├── test_project_routes.py          # interaction tests related to projects' endpoints
|   |   └── test_user_routes.py             # interaction tests related to users' endpoints
│   │    
│   ├── __init__.py                  
│   ├── Pipfile.toml                        # minimal configuration file dependencies
│   └── Pipfile.lock                        # json dependencies manager
│
|
├── client/
│   ├── task_manager_library/
│   │   ├── modules/
│   │   │   ├── __init__.py                 # manage functions' exportation
│   │   │   ├── project.py                  # project object class
│   │   │   ├── task.py                     # task object class
│   │   │   └── user.py                     # user object class
│   │   │
│   │   ├── __init__.py                     # manage functions' exportation
│   │   ├── config.py                       # configures the URL and HEADERS for HTTP requests
│   │   ├── http_client.py                  # functions to generate HTTP requests
│   │   ├── relationship_api.py             # functions to handle user-task and user-project relationships
│   │   ├── project_api.py                  # client-side functions for project-related HTTP operations
│   │   ├── task_api.py                     # client-side functions for task-related HTTP operations
│   │   ├── user_api.py                     # client-side functions for user-related HTTP operations
│   │   │
│   │   ├── aggregations.py                 # computes aggregations across modules
│   │   ├── statistic.py                    # compute general and user-specific statistics graphs
│   │   └── interface.py                    # provides command-line interface
│   │
│   ├── tests/
│   │   ├── __init__.py                     # manage functions' exportation
│   │   ├── test_project.py                 # class tests related to project object class
│   │   ├── test_task.py                    # class tests related to task object class
│   │   └── test_user.py                    # class tests related to user object class            
│   │
│   ├── setup.py                            # wheel setup
│   ├── task_manager_library.egg-info/      # wheel requirements folder
│   │   └── ...
│   ├── build/                              # wheel builder
│   │   └── lib/
│   │       └── ...
│   ├── dist/                               # wheel distributor
│   │   └── task_manager_lib....whl         # wheel package
│   │
│   ├── __init__.py                  
│   ├── Pipfile.toml                        # minimal configuration file dependencies
│   └── Pipfile.lock                        # json dependencies manager
|   
├── docs/
|   ├── er-schema.svg                       # ER schema made with mermaid
|   ├── Report.md                           # report documentation written in markdown
│   └── Report.pdf                          # same report exported as PDF
|
├── README.md                               # this file, provide repository instruction
└── .gitignore                              # files to ignore while pushing on the remote repository
```
## Key Files
* `backend/models`: defines all ORM classes used to create the database tables and enforce integrity constraints
* `backend/routes`: implements all HTTP endpoints and delegates core logic to the corresponding services
* `client/task_manager_library/modules`:  contains the client-side data classes used to model and interact with the system objects
* `client/task_manager_library/http_client.py`: provides generic functions to perform HTTP requests and handle responses, including error reporting and status feedback
* `client/task_manager_library/..._api.py`: offers high-level functions to interact with the system in an object-oriented style, provides python functions instead of calling an HTTP request manually
* `dist/task_manager_library-1.0.0-py3-none-any.whl`: Python wheel package generated for client distribution, the final packaged product
* `demo.py`: minimal working example that demonstrates how to use the library after installation

## API Overview
Quick overview:
| Project APIs              | Task APIs                  | User APIs              | Relationship APIs         | Aggregations/Statistics APIs   | Interface APIs              | Visualizations APIs           |
|:--------------------------|:---------------------------|:-----------------------|:--------------------------|:-------------------------------|:----------------------------| :-----------------------------|
| get_projects()            | get_tasks()                | get_users()            | assign_user_to_project()  | get_progress_by_tasks()        | project_interface()         | view_hours_task_project()     |
| get_project_by_id()       | get_task_by_id()           | get_user_by_id()       | assign_user_to_task()     | get_progress_by_project()      | task_interface()            | view_tasks_status_project()   |
| create_project()          | create_task()              | create_user()          | remove_user_from_task()   | get_total_hours_by_task()      | user_interface()            | view_tasks_priority_project() |
| update_project()          | update_task()              | update_user()          | remove_user_from_project()| get_total_hours_by_project()   |                             | show_project_summary_gui()    |
| delete_project()          | delete_task()              | delete_user()          | assign_project_to_user()  | get_total_hours_by_user()      |                             | show_gantt_gui()              |
| get_users_by_project()    | get_users_by_task()        | get_projects_by_user() | assign_task_to_user()     | get_hours_on_project_by_user() |                             |                               |
| get_tasks_by_project()    | get_project_by_task()      | get_tasks_by_user()    | remove_project_from_user()|                                |                             |                               |
| list_projects_all_status()| list_tasks_all_status()    |                        | remove_task_from_user()   |                                |                             |                               |
| list_projects_all_types() | list_tasks_all_priorities()|                        |                           |                                |                             |                               |

 ### # project APIs:
* `get_projects()` : retrieve a list of all `Project` instances from the database
* `get_project_by_id(project_id: int)` : retrieve a single `Project` by its unique ID
* `list_projects_all_status()` : retrieve all available project status labels as strings
* `list_projects_all_types()` : retrieve all available project type labels as strings
* `get_users_by_project(project: Project)` : retrieve the list of `User` instances assigned to a given `Project`
* `get_tasks_by_project(project: Project)` : retrieve the list of `Task` instances associated with a given `Project`
* `create_project(project: Project)` : create a new `Project` in the database and return the created instance
* `update_project(project: Project)` : update an existing `Project` in the database and return the updated instance
* `delete_project(project_id: int)` : delete the `Project` identified by the given ID

### # task APIs:
* `get_tasks()` : retrieve a list of all `Task` instances from the database
* `get_task_by_id(task_id: int)` : retrieve a single `Task` by its unique ID, including the associated `Project`
* `list_tasks_all_status()` : retrieve all available task status labels as strings
* `list_tasks_all_priorities()` : retrieve all available task priority levels as strings
* `get_project_by_task(task: Task)` : retrieve the `Project` associated with the given `Task`
* `get_users_by_task(task: Task)` : retrieve the list of `User` instances assigned to a given `Task`
* `create_task(task: Task)` : create a new `Task` in the database and return the created instance
* `update_task(task: Task)` : update an existing `Task` in the database and return the updated instance
* `delete_task(task_id: int)` : delete the `Task` identified by the given ID

### # user APIs:
* `get_users()` : retrieve a list of all `User` instances from the database
* `get_user_by_id(user_id: int)` : retrieve a single `User` by their unique ID
* `get_tasks_by_user(user: User)` : retrieve the list of `Task` instances assigned to the given `User`
* `get_project_by_user(user: User)` : retrieve the list of `Project` instances the given `User` is involved in
* `create_user(user: User)` : create a new `User` in the database and return the created instance
* `update_user(user: User)` : update an existing `User` in the database and return the updated instance
* `delete_user(user_id: int)` : delete the `User` identified by the given ID

### # user-project APIs:
* `assign_user_to_project(user, project, role=None)` : assign a `User` to a `Project`, optionally specifying a role
* `remove_user_from_project(user, project)` : remove a `User` from a `Project`
* `assign_project_to_user(project, user, role=None)` : assign a `Project` to a `User`, optionally specifying a role
* `remove_project_from_user(project, user)` : remove a `Project` from a `User`

### # user-task APIs:
* `assign_user_to_task(user, task, work_hours=None)` : assign a `User` to a `Task`, optionally specifying work hours
* `remove_user_from_task(task, user)` : remove a `User` from a `Task`
* `assign_task_to_user(task, user, work_hours=None)` : assign a `Task` to a `User`, optionally specifying work hours
* `remove_task_from_user(task, user)` : remove a `Task` from a `User`

### # project visualizations:
* `view_hours_task_project(project, width=10, height=6)` : pie chart of `work_hours` per task in the project
* `view_tasks_status_project(project, width=10, height=5, font_scale=3.0)` : bar chart of task status distribution in the project
* `view_tasks_priority_project(project, width=10, height=5, font_scale=3.0)` : bar chart of task priorities in the project
* `show_project_summary_gui(project)` : display a full-screen tkinter GUI with hours, status, and priority charts
* `show_gantt_gui(project)` : display an interactive Gantt chart using Plotly for the selected project

### # aggregations and statistics:
* `get_progress_by_tasks(tasks)` : return % of tasks marked as 'Completed'
* `get_progress_by_project(project)` : return % of completed tasks in the given project
* `get_total_hours_by_task(task)` : sum of work hours by all users assigned to the task
* `get_total_hours_by_project(project)` : total work hours across all tasks in the project
* `get_total_hours_by_user(user)` : total work hours across all tasks assigned to the user
* `get_hours_on_project_by_user(user, project)` : total work hours user spent on tasks in the given project

### # interfaces:
* `project_interface(project)` : display detailed project info, progress, user and task count using terminal color formatting
* `task_interface(task)` : display detailed task info including dates, cost, budget, project name, user count
* `user_interface(user)` : display detailed user info, assigned projects and tasks, and total work hours


---

---


## Main Setups
In the following lines you will find all the instructions to perform the main setups:
- [flask app and database](#setup-the-database--run-the-flask-app)
- [demo](#setup-and-run-the-demo)
- [tests](#run-tests)
- [export a new wheel version](#export-a-new-version-of-the-library)

***
## Setup the Database & Run the Flask App
### activate the backend pipenv
Open a terminal (e.g., PowerShell), navigate to the repository root `PS C:\Users\...\Group_06_Bernacchia_Fernandez>`, and run:
```
cd .\backend
pipenv shell
```
You should now see a prompt like:
```
(backend) PS C:\Users\...\backend>
```

Now you are in the path `PS C:\Users\...\Group_06_Bernacchia_Fernandez\backend` which is the location of the `Pipfile` TOML file with the virtual environment activated.
Then install the dependencies:
```
pipenv install
```
>&nbsp;
> To check if you're in the correct environment:
>```
>pipenv --venv
>```
> After this command it should appear a string like the following in the path. These means that you are in the correct environment.
>```
>C:\Users\...\.virtualenvs\backend-9WuIAnzU
>```
>&nbsp;


### run the Flask App
Navigate to the `app` folder and start the server:
```
cd .\app
python app.py
```


The app will create inside `PS C:\Users\...\backend\app>` a folder `instance`, containing the SQLite database and the output should show something like:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
It means that our app is online on the localhost and we can use it to make our HTTP requests.
Keep this terminal open to let the Flask app run in the background.

To stop it:
- to exit from the app : `CTRL+C` 
- to exit from the environment : `exit`

***
## Setup and Run the Demo
### activate the flask app
[follow the instructions here](#run-the-flask-app)
### activate the root pipenv
Open a terminal (e.g., PowerShell), navigate to the repository root `PS C:\Users\...\Group_06_Bernacchia_Fernandez>`, where you find the `Pipfile` TOML file of the virtual environment a run:
```
pipenv shell
pipenv install
```

### run the demo application
Then simply run:
```
python demo.py
```

***
## Run Tests

### Backend Tests
Test coverage: __125 interaction tests__ checking the behavior of HTTP endpoints with the DB.    
They run independently using pytest fixtures.

```
cd backend
pipenv shell
pipenv run pytest .\tests\
```

### Client Tests
Test coverage: __21 unit classes tests__ checking that client-side classes behave as expected.
No HTTP communication involved.
```
cd client
pipenv shell
pipenv run pytest .\tests\
```
***
## Export a New Version of the Library
You can create a new version of the client library using:
```
cd client
pipenv run python setup.py bdist_wheel
```
Then if necessary you can uninstall the old version
```
pipenv uninstall task-manager-library
```
Install the new version (adjust path if needed):
```
pipenv install .\dist\task_manager_library-0.1.1-py3-none-any.whl
```
***
## Change database service
If you want to switch to another database backend, update the logic inside the corresponding `*_service.py` files in:
```
backend/app/
```
These service files fully encapsulate the DB logic. Since the `routes` delegate to them, you won't need to change the route implementations.