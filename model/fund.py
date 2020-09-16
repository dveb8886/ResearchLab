import general.settings as settings

class Fund:

    def __init__(self, field_dict):
        self.id = field_dict["id"]
        self.prof = field_dict["prof"]
        self.fund_name = field_dict["fund_name"]
        self.fund_manager = field_dict["fund_manager"]
        self.fund_vintage = field_dict["fund_vintage"]
        self.fund_nav = field_dict["fund_nav"]
        self.fund_unfunded = field_dict["fund_unfunded"]

    def __str__(self):
        return "fund[" + str(self.id) + ": "+self.fund_name + "]"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def add(fund_name, fund_manager, fund_vintage, fund_nav, fund_unfunded, prof):
        id = settings.sql.fund_add(fund_name=fund_name, fund_manager=fund_manager, fund_vintage=fund_vintage, fund_nav=fund_nav, fund_unfunded=fund_unfunded, prof=prof)
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