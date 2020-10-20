import general.settings as settings


class Role:

    def __init__(self, field_dict):
        self.id = field_dict["id"]
        self.name = field_dict["name"]
        self.active = field_dict["active"]

    def __str__(self):
        return "role[" + str(self.id) + ": "+self.name + "]"

    def __repr__(self):
        return self.__str__()

    def get_resource(self):
        return 'role_'+self.id

    @staticmethod
    def add(name):
        id = settings.sql.role_add(name=name, active=1)
        return Role.find(id)

    @staticmethod
    def find(role_id):
        result = settings.sql.role_find(id=role_id)
        return None if result is None else Role(result)

    @staticmethod
    def find_byname(name):
        result = settings.sql.role_find_byname(name=name)
        return None if result is None else Role(result)

    def change(self, fields):
        pass