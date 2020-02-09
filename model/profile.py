import general.settings as settings

class Profile:

    def __init__(self, field_dict):
        self.id = field_dict["id"]
        self.org = field_dict["org"]
        self.prof_name = field_dict["prof_name"]

    def __str__(self):
        return "prof[" + str(self.id) + ": "+self.prof_name + "]"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def add(prof_name, org_id):
        id = settings.sql.prof_add(prof_name=prof_name, org=org_id)
        return Profile.find(id)

    @staticmethod
    def find(prof_id):
        result = settings.sql.prof_find(id=prof_id)
        return Profile(result)

    @staticmethod
    def list(org_id):
        lst = settings.sql.prof_list(org_id=org_id)
        result = []
        for item in lst:
            result.append(Profile(item))
        return result

    def change(self, fields):
        pass