import general.settings as settings
from model.base_mdl import BaseMdl


class Organization(BaseMdl):

    def __init__(self, field_dict):
        self.id = field_dict["id"]
        self.org_name = field_dict["org_name"]

    def __str__(self):
        return "org[" + str(self.id) + ": "+self.org_name + "]"

    def __repr__(self):
        return self.__str__()

    def get_resource(self):
        return 'org_'+str(self.id)

    @staticmethod
    def add(org_name):
        id = settings.sql.org_add(org_name=org_name)
        return Organization.find(id)

    @staticmethod
    def find(org_id):
        result = settings.sql.org_find(id=org_id)
        return Organization(result)

    @staticmethod
    def list():
        lst = settings.sql.org_list()
        result = []
        for item in lst:
            result.append(Organization(item))
        return result

    def change(self, fields):
        pass