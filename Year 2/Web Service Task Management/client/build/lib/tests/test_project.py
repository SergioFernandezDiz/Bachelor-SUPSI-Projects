from modules.project import Project


class TestProject:
    def test_init_minimal(self):
        project = Project(
            name="Test Project",
            project_type="Test Type"
        )
        assert project.id is None
        assert project._Project__name == "Test Project"
        assert project._Project__project_type == "Test Type"
        assert project._Project__project_status == "Behind"

    def test_init_complete(self):
        project = Project(
            name="Test Project",
            project_type="Test Type",
            project_status="On Track",
            project_id=1
        )
        assert project.id == 1
        assert project._Project__name == "Test Project"
        assert project._Project__project_type == "Test Type"
        assert project._Project__project_status == "On Track"

    def test_from_json_minimal(self):
        data = {
            "name": "Imported Project",
            "project_type": "Test Type"
        }
        project = Project.from_json(data)
        assert project.id is None
        assert project._Project__name == "Imported Project"
        assert project._Project__project_type == "Test Type"
        assert project._Project__project_status == "Behind"

    def test_from_json_complete(self):
        data = {
            "id": 10,
            "name": "Complete Imported Project",
            "project_type": "Test Type",
            "project_status": "Completed"
        }
        project = Project.from_json(data)
        assert project.id == 10
        assert project._Project__name == "Complete Imported Project"
        assert project._Project__project_type == "Test Type"
        assert project._Project__project_status == "Completed"

    def test_to_dict_minimal(self):
        project = Project(
            name="Minimal Project",
            project_type="Test Type"
        )
        d = project.to_dict()
        assert d["name"] == "Minimal Project"
        assert d["project_type"] == "Test Type"
        assert d["project_status"] == "Behind"
        assert "id" not in d

    def test_to_dict_complete(self):
        project = Project(
            name="Full Project",
            project_type="Test Type",
            project_status="Delayed",
            project_id=100
        )
        d = project.to_dict()
        assert d["id"] == 100
        assert d["name"] == "Full Project"
        assert d["project_type"] == "Test Type"
        assert d["project_status"] == "Delayed"

    def test_repr(self):
        project = Project(
            name="Repr Project",
            project_type="Test Type",
            project_status="At Risk",
            project_id=1000
        )
        s = repr(project)
        assert "PROJECT [1000]" in s
        assert "Repr Project" in s
        assert "type: Test Type" in s
        assert "status: At Risk" in s
