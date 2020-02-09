import general.settings as settings

class Fund:

    def __init__(self, field_dict):
        self.id = field_dict["id"]
        self.prof = field_dict["prof"]
        self.fund_name = field_dict["fund_name"]

    def __str__(self):
        return "fund[" + str(self.id) + ": "+self.fund_name + "]"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def add(fund_name, prof):
        id = settings.sql.fund_add(fund_name=fund_name, prof=prof)
        return Fund.find(id)

    @staticmethod
    def find(fund_id):
        result = settings.sql.fund_find(id=fund_id)
        return Fund(result)

    @staticmethod
    def list(prof_id):
        lst = settings.sql.fund_list(prof_id=prof_id)
        result = []
        for item in lst:
            result.append(Fund(item))
        return result

    def change(self, fields):
        pass