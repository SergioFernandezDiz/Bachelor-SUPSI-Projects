from modules.user import User

class TestUser:

    def test_init_minimal(self):
        user = User(
            username="jane_doe",
            name="Jane",
            last_name="Doe"
        )
        assert user.id is None
        assert user._User__username == "jane_doe"
        assert user._User__name == "Jane"
        assert user._User__last_name == "Doe"

    def test_init_complete(self):
        user = User(
            username="jane_doe",
            name="Jane",
            last_name="Doe",
            user_id=1
        )
        assert user.id == 1
        assert user._User__username == "jane_doe"
        assert user._User__name == "Jane"
        assert user._User__last_name == "Doe"

    def test_from_json_minimal(self):
        data = {
            "username": "jane_doe",
            "name": "Jane",
            "last_name": "Doe"
        }
        user = User.from_json(data)
        assert user.id is None
        assert user._User__username == "jane_doe"
        assert user._User__name == "Jane"
        assert user._User__last_name == "Doe"

    def test_from_json_complete(self):
        data = {
            "id": 10,
            "username": "jane_doe",
            "name": "Jane",
            "last_name": "Doe"
        }
        user = User.from_json(data)
        assert user.id == 10
        assert user._User__username == "jane_doe"
        assert user._User__name == "Jane"
        assert user._User__last_name == "Doe"

    def test_to_dict_minimal(self):
        user = User(
            username="jane_doe",
            name="Jane",
            last_name="Doe"
        )
        d = user.to_dict()
        assert d["username"] == "jane_doe"
        assert d["name"] == "Jane"
        assert d["last_name"] == "Doe"
        assert "id" not in d

    def test_to_dict_complete(self):
        user = User(
            username="jane_doe",
            name="Jane",
            last_name="Doe",
            user_id=100
        )
        d = user.to_dict()
        assert d["id"] == 100
        assert d["username"] == "jane_doe"
        assert d["name"] == "Jane"
        assert d["last_name"] == "Doe"

    def test_repr(self):
        user = User(
            username="jane_doe",
            name="Jane",
            last_name="Doe",
            user_id=1000
        )
        s = repr(user)
        assert "USER [1000]" in s
        assert "@jane_doe" in s
        assert "name: Jane" in s
        assert "last name: Doe" in s
