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

    @staticmethod
    def find_byresource(resource):
        lst = settings.sql.get_roles_by_resource(resource=resource+'%')
        result = []
        for item in lst:
            result.append(Role(item))
        return result

    @staticmethod
    def get_role_assignments_for_users(users, roles):
        user_ids = [x.id for x in users]
        role_ids = [x.id for x in roles]
        lst = settings.sql.get_user_role_assignments(user_ids=user_ids, role_ids=role_ids)
        result = {u: {r: False for r in role_ids} for u in user_ids}
        for item in lst:
            result[item['user_id']][item['role_id']] = True
        return result

    @staticmethod
    def get_all_role_assignments_for_roles(roles):
        role_ids = [x.id for x in roles]
        lst = settings.sql.get_role_assignments(role_ids=role_ids)
        result = {}
        for item in lst:
            user_id = item['user_id']
            role_id = item['role_id']
            if user_id not in result:
                result[user_id] = {r: False for r in role_ids}
            result[user_id][role_id] = True
        return result

    def change(self, fields):
        pass