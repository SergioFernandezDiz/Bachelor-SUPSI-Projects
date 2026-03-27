    Group_06_Bernacchia_Fernandez
# WEB SERVICE - Task Manager
## Abstract
This report explores the design and implementation of a web service dedicated to task management, inspired by tools such as _Trello_ and _GitLab_. The motivation stems from the increasing need for ***coordination and clarity in project workflows***, especially within teams. After defining the problem and analyzing the existing solutions (_state of the art_), we present our technical approach, built around a __SQLite database__, __Flask backend__, and a __Python client library__. The project demonstrates a functional and user-friendly API with statistical insights, offering a foundational solution to distributed task tracking and management. The resulting architecture promotes __modularity, testability, and ease of use__, and provides a solid starting point for further development in real-world collaborative contexts.

## Introduction
_mettere link alla sezione corrispondente_
This report is structured in several chapters, each addressing a different aspect of the project development process:
1.  [__Motivation and Context__](#1-motivation-and-context)<br>
    _explains the relevance of task management tools in modern work environments_
2. [__Problem__](#2-problem)<br>
    _defines the problem tackled and its key aspects_
3. [__State of the Art__](#3-state-of-the-art)<br>
    _provides an overview of existing solutions and how our work relates to them_
4. [__Appoach to the problem__](#4-approach) <br>
    _details our methodology, from data storage to API implementation_<br>
        1. [data storage - SQLite](#41-data-storage---sqlite-database)<br>
        2. [backend - Flask App](#42-requests-and-backend---flask-app)<br>
        3. [API - Python client](#43-api---python-client)<br>
        4. [distribution - Wheel library](#44-distribution---wheel-package)<br>
5. [__Results__](#5-results)<br>
    _presents the outcomes of our implementation and testing (including a small demo app)_
6. [__Future Improvements__](#6-future-improvements)<br>
    _suggests potential enhancements to extend functionality, usability, and scalability of the system_
6. [__Conclusion__](#7-conclusions)<br>
    _summarizes contribution, scope, and limitations of the work in relation to the state of the art_

## 1. Motivation and Context
Cooperation and coordination are essential ingredients for team success. While small teams can easily manage tasks informally, as projects grow in size and complexity, the need for structured task tracking tools becomes critical. In this context, a simple, fast, and user-friendly web service can greatly improve project transparency and individual accountability.
Our goal was to create such a tool: a backend service capable of storing task data in a SQLite database, and providing endpoints for users to retrieve, update, and manage this data efficiently. To enrich the user experience, we also integrated a set of basic statistical features, available through a Python API.

## 2. Problem
This project targets any collaborative environment in which a project can be divided into individual tasks. More specifically, it is structured around the [@JohnVans123/ProjectManagementDataset](https://huggingface.co/datasets/JohnVans123/ProjectManagement), which models a variety of projects, each composed of multiple tasks assigned to users.
 
 Each Task is represented as a row in a table, with fields such as:
| Task ID | Task Name | Task Status | Assigned To | Hours spent | Budget | Actual Cost | Progress | Location | Start Date | End Date | Project ID | Project Name | Project Type |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

We adapted this dataset to model a collaborative system where multiple users can take part in projects (instead of only one), assign themselves tasks, and update task statuses. This framework can also serve as a personal or professional project history, supporting performance tracking and resume building. Leaving always the team up to date to the modification applied and the progress gained.

## 3. State of the Art
This is primarily a __didactic project__, aimed at _applying and consolidating the knowledge_ acquired in the course. One requirement was to use GitLab, which also offers built-in task planning tools. Inspired by [__GitLab's Plan__](https://about.gitlab.com/) section and by [__Trello__](https://trello.com/home), a popular task management platform, we aimed to replicate a minimal, extensible version of such tools.
Although our implementation is far less complex than Trello, we restructured the dataset to create a functional and coherent service that supports data access, team coordination, and progress visualization.

## 4. Approach to the problem
First, we divided the web service creation into manageable issues (tasks) and designed specific solutions for each component:
1. [data storage](#41-data-storage---sqlite-database) &nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp;&nbsp;__SQLite database__ 
2. [backend](#42-requests-and-backend---flask-app) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp; __Flask app with CRUD endpoints__
3. [API](#43-api---python-client)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp;__object-oriented Python client__
4. [distribution](#44-distribution---wheel-package)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;&nbsp;&nbsp;&nbsp;__`wheel` library permitting the usage of the api__


### 4.1 data storage - SQLite database
***
The first issue to address was where to store the data provided by the user. Since this is a university project, unlikely to require high scalability or heavy concurrent access, we opted for __SQLite__ as our database.

> [***SQLite***](https://sqlite.org/) is a lightweight, serverless database engine widely used for prototyping and small-scale applications.

SQLite is natively supported in Python and has a straightforward setup, making it ideal for rapid development and easy integration with our web service. It doesn’t require a separate server process, and all data is stored in a single file, which makes it very convenient for local testing and development.

Given that the project required exposing data through an API, we also decided to use __Flask__, the Python web micro-framework.
>[***Flask***](https://flask.palletsprojects.com/) is a Python micro-framework ideal for building web services and REST APIs. 

Flask is lightweight, well-documented, and integrates smoothly with SQLite and SQLAlchemy. Its simplicity allows us to focus on the core functionality of the web service while keeping the codebase minimal and readable. For our needs (CRUD operations, relational data exposure, and simple statistics) Flask is a pragmatic and efficient solution.

***
We adapted  and extended the [HuggingFace dataset](https://huggingface.co/datasets/JohnVans123/ProjectManagement), normalizing it into multiple tables to improve data management and enforce logical relationships. For example, we  manually added user `roles` per project and allowed multiple `users` per `task`, resulting in a more realistic and flexible data model.

| We defined three strong entities |     | with two many-to-many relationships|
| :------------------------------- | --- | :--------------------------------- |
| __User__                         |     | __User__ &rlarr; __Project__       |
| __Project__                      |     |__User__ &rlarr; __Task__           |
| __Task__                         |     |                                    |

Each many-to-many relationship was modeled as a separate association table. Every table has a primary key and one or more foreign keys, typically referencing fixed options or pre-defined categories (e.g., user roles).

The resulting Entity-Relationship Diagram is shown below:
![Schema](../docs/er-schema.svg)
Each table was mapped to a SQLAlchemy __model__ to manage integrity constraints and enable object-relational mapping (_ORM_). This approach allows us to interact with the database using _Python classes_ and ensures consistent data structure and validation across the application.

The [HuggingFace dataset](https://huggingface.co/datasets/JohnVans123/ProjectManagement) was used to populate the backend from the start, enabling iterative testing and validation of how the application behaves in a realistic context. 

### 4.2 requests and backend - Flask App
After defining the __models__, we passed them to a dedicated __service__ layer, which _handles all the queries to the database_. This layer implements the full set of __CRUD operations__ (Create, Read, Update, and Delete) for each entity. It serves as a clean interface between the database and the application logic, ensuring that all interactions with the data are handled in a _consistent_ and _maintainable_ way.

All the services are then used inside the __Flask App's routes__, which expose _API endpoints_ for external access via _HTTP requests_.
***
This separation of concerns allows us to modularize the backend:
* __routes__ handle the request logic
* __services__ handle data access
* __models__ enforce structure and constraints

Using Flask also made it easy to continuously test the API during development. We relied heavily on __Postman__, a collaboration platform for API development and testing.

> [***Postman***](https://www.postman.com/) allows developers to test API endpoints through a user-friendly interface, automate request sequences, verify response correctness, and debug errors efficiently.
<br>
***
As a result, we developed a fully functional __backend__ capable of retrieving and manipulating structured data through a clean and extensible __REST API__.

>[***RE****presentational* ***S****tate* ***T****ransfer* ***API***](https://restfulapi.net/) is an architectural style for designing networked applications. <br> It relies on standard HTTP methods (GET, POST, PUT, DELETE) to interact with resources identified by URLs. <br> REST APIs are stateless, scalable, and language-independent, making them ideal for web services and client-server communication.

To ensure that the entire system worked correctly under different scenarios, we conducted __interaction testing__ using the __pytest__ framework.

> ***interaction testing*** ensures components (e.g. services, models, and routes) interact correctly under various conditions and that application logic behaves as expected across modules.

> [***Pytest***](https://docs.pytest.org/) is a powerful testing framework for Python, known for its simplicity and flexibility.

We implemented __125 tests__, covering:
- _input validation_<br>
    e.g. field types, keys ignored during posts, primary keys inserted...
- _error handling_<br>
    e.g. non-existent user IDs, non-existent relationship, invalid field for defined foreign keys...
- _consistency of changes across services_

Each test ensures correct request behavior and proper database updates or error returns.

### 4.3 API - python client
This component represents the actual product designed for the client: _a package that provides all the necessary functions by interacting with the backend through its routes_.
The __client-side API__ exposes all the functionalities required to _fetch, update, manipulate_, and _delete_ data from the database.

The key difference between the client and the backend lies in the implementation style: the client is ***fully object-oriented***. This means that the user can interact with the database entirely through __Python classes and functions__, without having to deal directly with HTTP requests or low-level backend logic.

The client library is structured into __modules__, each of which contains _Python classes_ representing the core entities: __User, Project__, and __Task__. These mirror the backend models and are designed to be initialized and used directly when interacting with the API.

Each class provides:
- a __class method__ that converts a _JSON response_ from the backend into a proper _Python object_ (handling default or missing fields gracefully),
- an _instance method_ that does the reverse: converts a _class instance_ into a _dictionary_ suitable for serialization and use as the body of a _POST or PUT HTTP request_.

A key design principle is that these classes are _"dumb"_: they contain no embedded logic for HTTP communication. Instead, all communication is handled by the API layer, making the architecture _clean and modular_.

The API client includes four core types of methods:

- `GET`: these functions either return a __full list of objects of a given type__ (with no arguments) or retrieve a __specific object__ using its id. Under the hood, these make _GET requests_ to the appropriate backend route.
- `CREATE`: these functions accept an object instance and use a _POST request_ to __create the corresponding entity in the database__. The backend returns the __created object__, now including its assigned id.
- `UPDATE`: these require an object with a valid id. They make a _PUT request_ to __update the corresponding entity in the database__ with the new data.
- `DELETE`: these take an id and __remove the corresponding entity from the database__.

***
#### Relationship Handling
Many-to-many relationships (e.g. between `User` and `Project`, or `User` and `Task`) are handled slightly differently. These associations are _"silent"_, they cannot be retrieved directly via a dedicated endpoint, but they are visible indirectly:
_For example, when requesting all projects of a user, or all users of a project, the role attribute in the relationship is included in the result._

To create or modify these relationships, a _POST request_ is made with both involved `entities` and the `role`. If the relationship already exists, it is __updated__; if not, it is __created__.

***
#### Response Integrity & Feedback
Since the `entity classes` themselves are decoupled from the live state of the database, __inconsistencies__ could occur. To prevent this, every API `response` is passed through the `terminal_response` function.

This function:
- prints a __success message__ to the terminal and continues execution if the operation succeeded,
- raises an __exception__ and interrupt the program execution if an error is returned by the backend,
- prints a __warning__ but continues execution in case of non-fatal issues (e.g., ignored keys in an update request).

This mechanism ensures __data consistency__ and immediate __feedback__ during usage.

***
#### Unit Tests
The client module was tested with __22 class-level unit tests__, validating that:
- `constructors` work correctly with both full and partial parameters,
- `JSON-to-object` and `object-to-dictionary` conversions behave as expected.

Although __mock tests__ would have been appropriate to simulate backend interactions, due to time constraints and their non-mandatory nature for the deliverables, they were deferred and listed among the possible future improvements.
> [***mock testing***](https://en.wikipedia.org/wiki/Mock_object) simulate external dependencies (e.g., APIs) using mock objects to enable isolated testing.

***
#### Additional Modules
To further enrich the client capabilities, three additional modules were developed:
- `aggregations.py`: provides aggregated data such as the _overall progress of a project_ (as percentage of completed tasks) or the _total hours a user has worked on a project_ or in _general_.
- `statistics.py`: contains _visualizations_ to offer high-level insights into the database contents; such as: _task status distributions within a project_, _each user's contribution in percentage_ and a _Gantt chart of a specific project's tasks_.
- `interface.py`: offers _simple textual overviews_ of data related to specific entities, improving the readability of API outputs.


### 4.4 distribution - wheel package
The project has been finalized as a distributable __Python library__ using the __wheel packaging system__, as introduced during the course.
> [***Wheel***](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) is a built-package format for Python, intended to speed up installations and make package management more reliable.

This approach was ideal in our case, as it allowed us to __isolate and export__ only the `task_manager_library` folder, making it easily installable and reusable in other Python projects.

To demonstrate and validate the functionalities of our library, we also developed a small __demo application__ named `demo.py`. This script showcases a _minimal working example using the client API_.

In the current implementation, our backend runs with a _pre-filled database_ using the [HuggingFace dataset](https://huggingface.co/datasets/JohnVans123/ProjectManagement). However, in a real-world deployment, the system would typically start with an _empty database_ that the user populates over time.   
For demonstration purposes, having pre-populated data is essential to effectively showcase the API's capabilities.

## 5. Results
The final product consists of a __fully functional and tested task management system__, composed of:
- a __Flask-based REST API__, capable of handling ***CRUD operations*** across all key entities (`Users`, `Projects`, `Tasks`), with consistent validation and robust error handling.
- A __SQLite database__ organized in a ***relational schema with many-to-many relationships***, enhanced with foreign keys, constraints, and realistic normalization.
- A __Python client library__, fully ***object-oriented***, offering a high-level abstraction over the backend logic and enabling seamless interaction with the API.
- A suite of about __150 automated tests__ using `pytest`, ensuring correctness of functionality, interaction consistency, and robustness under a wide range of input scenarios.
- A sample __demo script__, illustrating basic workflows such as project creation, user-task assignment, and status updates.

We validated the system by simulating typical user interactions, including:
- Creating users and assigning them to multiple projects.
- Defining tasks with deadlines and costs.
- Tracking project progress and user workload.
- Extracting basic statistics, such as completion rates and total budget spent per project.

The results confirm that the application is __capable of supporting basic task management workflows efficiently and intuitively__.    
The architecture also supports future extensions without major restructuring.

## 6. Future improvements
Due to ***time constraints***, the project was not developed as thoroughly as we would have been capable of. Several functionalities that could have enriched and completed the application are currently missing.
- __Additional Aggregations and Statistics__: we did not have enough time to design and implement further aggregations or statistics to visualize. It would have been interesting to develop some predictive models based on user-provided data—for instance, providing personalized predictions on the estimated time a specific user might need to complete a task, or similar insights.
- __Enhanced Visualization and Dashboards__: as for the statistics and interface, it would have been valuable to implement dashboards for each entity type. This would allow combining data visualizations with interface panels displaying entity-specific information. At present, the related functionalities are limited to `interface.py` and could be extended and integrated more comprehensively into the overall client. Plus we noticed, that inside `statistic.py`, there is an issue inside the `show_project_summary_gui`, infact we weren't able to understand how exit from the loop...
- __Complete Testing Suite__: from a development and software engineering perspective, completing the testing suite would be essential for a real-world or long-term deployment.
In particular, the project would benefit from:
    - ***Unit tests for backend services***,
    - ***Interaction tests for the Python client API***,
        possibly including mock databases to simulate and validate endpoint behavior.
- __Scalability and Database Optimization__: lastly, if the application were to scale to a larger user base and data volume, the current service and database (__SQLite__) may not be optimal. During the implementation of certain statistical functions, we noticed that __SQLite__ can be quite slow for more complex operations over larger datasets. In such a scenario, it would be worth considering switching to a more performant database system and updating the `service` logic accordingly.

## 7. Conclusions
This project delivered a __modular and extensible web service for task management__, tailored for team collaboration and progress monitoring. The use of __SQLite__, __Flask__, and an object-oriented __Python client__ allowed us to focus on clarity, maintainability, and testability throughout the development process.

Compared to existing tools such as __Trello__ and __GitLab’s Plan section__, our solution is deliberately __minimal__, but it captures the essential mechanics of collaborative task assignment and tracking. The separation between backend logic, database, and client API encourages clean architecture and simplifies further development or deployment.

While the current implementation is ***suitable for academic or small-team contexts***, future improvements (e.g., user authentication, UI integration, advanced analytics) could bring the system closer to production-level quality.

Ultimately, the project highlights the value of structured planning, modular design, and testing in the development of even small-scale software systems. It serves as a concrete application of the software engineering principles studied in the course and a foundation for future exploration.

