
class User:
    def __init__(self, username:str, name:str, last_name:str, user_id:int = None, role:str = None, work_hours:int = 0):
        self.__id = user_id
        self.__username = username
        self.__name = name
        self.__last_name = last_name
        self.__role = role
        self.__work_hours = work_hours

    @classmethod
    def from_json(cls, data:dict):
        return cls(
            user_id = data['id'] if data.get('id') else None,
            username = data['username'],
            name = data['name'],
            last_name = data['last_name'],
            role = data['role'] if data.get('role') else 'Normal',
            work_hours = data['work_hours'] if data.get('work_hours') else 0
        )

    def to_dict(self):
        user_dict = {
            'username': self.__username,
            'name': self.__name,
            'last_name': self.__last_name
        }
        if self.__id is not None:
            user_dict['id'] = self.__id
        if self.__role is not None:
            user_dict['role'] = self.__role
        #if self.__work_hours is not None:
        #    user_dict['work_hours'] = self.__work_hours

        return user_dict

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def last_name(self):
        return self.__last_name
    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def role(self):
        return self.__role
    @role.setter
    def role(self, value):
        self.__role = value

    @property
    def work_hours(self):
        return self.__work_hours
    @work_hours.setter
    def work_hours(self, value):
        self.__work_hours = value


    def __repr__(self):
        return f'USER [{self.__id}] @{self.__username} = \tname: {self.__name}, last name: {self.__last_name}'