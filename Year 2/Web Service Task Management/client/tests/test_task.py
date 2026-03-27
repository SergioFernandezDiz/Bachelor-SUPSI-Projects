#Group_06_Bernacchia_Fernandez\client> pipenv run pytest tests/
from datetime import datetime, timedelta
from modules.task import Task


class DummyProject:
    def __init__(self, project_id):
        self.__id = project_id

    @property
    def id(self):
        return self.__id


class TestTask:
    def test_init_minimal(self):
        task = Task(
            name="Test Task",
            location="Test Location",
            status="Pending"
        )
        now = datetime.now()
        delta = now - task.start_date
        assert delta < timedelta(seconds=1)

        assert task.id is None
        assert task.name == "Test Task"
        assert task.location == "Test Location"
        assert task.status == "Pending"
        assert task.priority == "Low"

    def test_init_complete(self):
        project = DummyProject(1)
        start_fixed_date = datetime(2024, 5, 20, 12, 0, 0)
        end_fixed_date = datetime(2024, 6, 20, 12, 0, 0)
        task = Task(
            name="Task Complete",
            location="Office",
            status="Ongoing",
            start_date=start_fixed_date,
            task_id=42,
            priority="High",
            end_date=end_fixed_date,
            actual_cost=123.45,
            budget=150.0,
            project_id=project.id,
            work_hours=123.45
        )
        assert task.id == 42
        assert task.actual_cost == 123.45
        assert task.budget == 150.0
        assert task.project_id == 1
        assert task.priority == "High"
        assert task.start_date == start_fixed_date
        assert task.end_date == end_fixed_date
        assert task.work_hours == 123.45

    def test_from_json_minimal(self):
        data = {
            "name": "Imported Task",
            "location": "Remote",
            "status": "Done"
        }
        task = Task.from_json(data)
        assert task.name == "Imported Task"
        assert task.status == "Done"
        assert task.priority == "Low"
        assert task.work_hours == 0
        assert task.project_id == None
        assert task.id == None

    def test_from_json_complete(self):
        data = {
            "id": 10,
            "name": "Complete Imported Task",
            "location": "Remote",
            "start_date": "2024-05-10T10:00:00",
            "status": "Done",
            "priority": "Medium",
            "end_date": "2024-05-15T10:00:00",
            "actual_cost": 75.0,
            "budget": 100.0,
            "project_id": 10,
            "work_hours": 123.45
        }
        task = Task.from_json(data)
        assert task.id == 10
        assert task.name == "Complete Imported Task"
        assert task.priority == "Medium"
        assert task.status == "Done"
        assert task.start_date == datetime.fromisoformat("2024-05-10T10:00:00")
        assert task.end_date == datetime.fromisoformat("2024-05-15T10:00:00")
        assert task.actual_cost == 75.0
        assert task.budget == 100.0
        assert task.project_id == 10
        assert task.work_hours == 123.45

    def test_to_dict_minimal(self):
        project = DummyProject(5)
        task = Task(
            name="Minimal Task",
            location="Nowhere",
            status="New",
            start_date=datetime(2024, 5, 20),
            project_id=project.id
        )
        d = task.to_dict()
        assert d["name"] == "Minimal Task"
        assert d["location"] == "Nowhere"
        assert d["status"] == "New"
        assert d["priority"] == "Low"
        assert d["project_id"] == 5
        assert "id" not in d
        assert "end_date" not in d

    def test_to_dict_complete(self):
        project = DummyProject(2)
        task = Task(
            name="Full Task",
            location="Here",
            status="Closed",
            start_date="2024-05-01T12:00:00",
            end_date="2024-05-10T12:00:00",
            actual_cost=99.99,
            budget=120.00,
            task_id=99,
            project_id=project.id,
            priority="High",
            work_hours=123.45
        )
        d = task.to_dict()
        assert d["id"] == 99
        assert d["actual_cost"] == 99.99
        assert d["budget"] == 120.00
        assert d["end_date"] == "2024-05-10T12:00:00"

    def test_repr(self):
        task = Task(
            name="Debug Task",
            location="Lab",
            status="Testing",
            start_date=datetime(2024, 5, 20),
            end_date=datetime(2024, 5, 25),
            task_id=11
        )
        s = repr(task)
        assert "TASK [11]" in s
        assert "Debug Task" in s
        assert "Testing" in s