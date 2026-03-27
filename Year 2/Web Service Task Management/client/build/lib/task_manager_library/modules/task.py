from datetime import date, datetime

from task_manager_library.http_client import get, terminal_response
from .project import Project

class Task:
    def __init__(self, name:str, location:str, status:str, start_date:datetime = datetime.now(), task_id:int = None, priority:str = "Low", end_date:datetime = None, actual_cost:float = None, budget:float = None, project_id:int=None, work_hours:float = 0):
        self.__id = task_id
        self.__name = name
        self.__location = location
        self.__start_date = start_date

        self.__status = status
        self.__priority = priority

        self.__start_date = datetime.fromisoformat(start_date) if isinstance(start_date, str) else start_date
        self.__end_date = datetime.fromisoformat(end_date) if isinstance(end_date, str) else end_date

        self.__actual_cost = actual_cost
        self.__budget = budget

        # class is stupid, it doesn't know whether a project exists
        self.__project_id = project_id

        self.__work_hours = work_hours


    @classmethod
    def from_json(cls, data: dict):
        return cls(
            task_id=data['id'] if data.get('id') else None,
            name=data['name'],
            location=data['location'],
            start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else datetime.now(),
            status=data['status'],
            priority=data['priority'] if data.get('priority') else 'Low',
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
            actual_cost=data.get('actual_cost') if data.get('actual_cost') else 0,
            budget=data.get('budget') if data.get('budget') else 0,
            project_id= data.get('project_id') if data.get('project_id') else None,
            work_hours=data.get('work_hours') if data.get('work_hours') else 0,
        )

    def to_dict(self):
        task_dict = {
            'name': self.__name,
            'location': self.__location,
            'start_date': self.__start_date.isoformat() if isinstance(self.__start_date, datetime) else self.__start_date,
            'project_id': self.__project_id,
            'status': self.__status,
            'priority': self.__priority
        }
        if self.__id is not None:
            task_dict['id'] = self.__id
        if self.__end_date is not None:
            task_dict['end_date'] = self.__end_date.isoformat() if isinstance(self.__end_date, datetime) else self.__end_date
        if self.__actual_cost is not None:
            task_dict['actual_cost'] = float(self.__actual_cost)
        if self.__budget is not None:
            task_dict['budget'] = float(self.__budget)
        if self.__work_hours is not None:
            task_dict['work_hours'] = float(self.__work_hours)

        return task_dict

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def priority(self):
        return self.__priority
    @priority.setter
    def priority(self, value):
        self.__priority = value

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def work_hours(self):
        return self.__work_hours
    @work_hours.setter
    def work_hours(self, value):
        self.__work_hours = value

    @property
    def start_date(self):
        return self.__start_date
    @start_date.setter
    def start_date(self, value):
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date
    @end_date.setter
    def end_date(self, value):
        self.__end_date = value

    @property
    def location(self):
        return self.__location
    @location.setter
    def location(self, value):
        self.__location = value

    @property
    def actual_cost(self):
        return self.__actual_cost
    @actual_cost.setter
    def actual_cost(self, value):
        self.__actual_cost = value

    @property
    def budget(self):
        return self.__budget
    @budget.setter
    def budget(self, value):
        self.__budget = value

    @property
    def project_id(self):
        return self.__project_id
    @project_id.setter
    def project_id(self, value):
        self.__project_id = value

    def __repr__(self):
        return f'TASK [{self.__id}] -- {self.__name} ({self.__start_date}, {self.__end_date}) = \t status: {self.__status}, priority: {self.__priority}, work_hours: {self.__work_hours}'