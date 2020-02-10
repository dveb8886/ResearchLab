import general.settings as settings

class Stat:

    def __init__(self, field_dict, values='db'):
        self.id = field_dict["id"]
        self.fund = field_dict["fund"]
        self.stat_name = field_dict["stat_name"]
        self.color_line = field_dict["color_line"]
        self.color_fill = field_dict["color_fill"]
        if values == None:
            self.values = [[], []]
        elif values == 'db':
            self.retrieve_stored_values()
        else:
            self.set_values(values)

    def __str__(self):
        return "stat[" + str(self.id) + ": "+self.stat_name + "]"

    def __repr__(self):
        return self.__str__()

    # retrieves from database and updates local
    def retrieve_stored_values(self):
        lst = list(settings.sql.stat_readvalues(stat_id=self.id))
        result = [[], []]
        for item in lst:
            result[0].append(item["x_date"])
            result[1].append(item["y_value"])
        self.values = result

    # simply reads from local
    def get_values(self):
        return self.values

    def get_y(self, index):
        return self.values[1][index]

    def commit(self):
        params = {
            'stat_id': self.id,
            'stat_name': self.stat_name,
            'color_line': self.color_line,
            'color_fill': self.color_fill
        }
        settings.sql.stat_update(**params)

    def set_color(self, r, g, b):
        self.color_line = 'rgba({}, {}, {}, {})'.format(r, g, b, '1.0')
        self.color_fill = 'rgba({}, {}, {}, {})'.format(r, g, b, '0.2')

    # updates the local value, but not the database
    def set_values(self, values):
        # validation
        if not isinstance(values, list) or len(values) != 2:
            raise ValueError('values is not a 2 dimensional list, submit it in the form of [[x1, x2, x3], [y1, y2, y3]]')
        x = values[0]
        y = values[1]
        if not len(x) == len(y):
            raise ValueError('len(x) is '+str(len(x))+', len(y) is '+str(len(y))+', but both should be the same length')
        self.values = values

    # writes the local values to the database
    def commit_values(self):
        settings.sql.stat_clearvalues(stat_id=self.id)
        for i in range(len(self.values[0])):
            settings.sql.value_add(stat=self.id, x_date=self.values[0][i], y_value=self.values[1][i])

    @staticmethod
    def add(stat_name, fund):
        result = settings.sql.stat_find_by_name(stat_name=stat_name, fund=fund)
        if not result == None:
            raise ValueError('this fund already has a stat called '+stat_name)
        id = settings.sql.stat_add(stat_name=stat_name, fund=fund)
        stat = Stat.find(id)
        stat.set_color(0, 0, 0)
        stat.commit()
        return stat

    @staticmethod
    def find(stat_id):
        result = settings.sql.stat_find(id=stat_id)
        return Stat(result)

    @staticmethod
    def find_by_name(stat_name, fund, values='db'):
        result = settings.sql.stat_find_by_name(stat_name=stat_name, fund=fund)
        if result == None:
            return None
        else:
            return Stat(result, values)

    @staticmethod
    def list(fund_id):
        lst = settings.sql.stat_list(fund_id=fund_id)
        result = []
        for item in lst:
            result.append(Stat(item))
        return result

    def change(self, fields):
        pass