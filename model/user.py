import general.settings as settings
from flask_login import UserMixin
from model.role import Role
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):

    def __init__(self, field_dict):
        self.id = field_dict["id"]
        self.username = field_dict["username"]
        self.password = field_dict["password"]

    def __str__(self):
        return "user[" + str(self.id) + ": "+self.username + "]"

    def __repr__(self):
        return self.__str__()

    def get_resource(self):
        return 'user_'+self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)
        settings.sql.user_changepass(id=self.id, password=self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_to_role(self, role_name=None, role_id=None):
        if role_id is None:
            role = Role.find_byname(role_name)
            if role is None:
                raise ValueError('There is no role by the name of {role}'.format(role=role_name))
            role_id = role.id
        settings.sql.user_add_to_role(user_id=self.id, role_id=role_id)

    def remove_from_role(self, role_name=None, role_id=None):
        if role_id is None:
            role = Role.find_byname(role_name)
            if role is None:
                raise ValueError('There is no role by the name of {role}'.format(role=role_name))
            role_id = role.id
        settings.sql.user_remove_from_role(user_id=self.id, role_id=role_id)

    def list_roles(self):
        lst = settings.sql.user_get_roles(user_id=self.id)
        result = []
        for item in lst:
            result.append(Role(item))
        return result

    @staticmethod
    def add(username, password):
        id = settings.sql.user_add(username=username)
        user = User.find(id)
        user.set_password(password)
        return user

    @staticmethod
    def find(user_id):
        result = settings.sql.user_find(id=user_id)
        return None if result is None else User(result)

    @staticmethod
    def find_byname(username):
        result = settings.sql.user_find_byname(username=username)
        return None if result is None else User(result)


    def change(self, fields):
        pass