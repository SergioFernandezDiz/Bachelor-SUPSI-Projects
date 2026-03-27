

class Project:
    def __init__(self, name:str, project_type: str, project_status: str = 'Behind', project_id:int = None, user_role: str='Normal'):
        self.__id = project_id
        self.__name = name
        self.__project_type = project_type
        self.__project_status = project_status
        self.__user_role = user_role

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def project_type(self):
        return self.__project_type
    @project_type.setter
    def project_type(self, value):
        self.__project_type = value

    @property
    def project_status(self):
        return self.__project_status
    @project_status.setter
    def project_status(self, value):
        self.__project_status = value

    @property
    def user_role(self):
        return self.__user_role
    @user_role.setter
    def user_role(self, value):
        self.__user_role = value

    @classmethod
    def from_json(cls, data:dict):
        return cls(
            project_id = data['id'] if data.get('id') else None,
            name = data['name'],
            project_type = data['project_type'],
            project_status = data['project_status'] if data.get('project_status') else 'Behind',
            user_role = data['role'] if data.get('role') else 'Normal'
        )


    def to_dict(self):
        project_dict = {
            'name': self.__name,
            'project_type': self.__project_type
        }
        if self.__id is not None:
            project_dict['id'] = self.__id
        if self.__project_status is not None:
            project_dict['project_status'] = self.__project_status
        if self.__user_role is not None:
            project_dict['user_role'] = self.__user_role

        return project_dict

    def __repr__(self):
        return f'PROJECT [{self.__id}] -- {self.__name} = \ttype: {self.__project_type}, status: {self.__project_status}'