from model.user import User
from model.role import Role

class AccountController():

    def __init__(self):
        pass

    def user_search(self, search_term, resource):
        roles = Role.find_byresource(resource)
        if search_term == '*':
            role_assignments = Role.get_all_role_assignments_for_roles(roles)
            users = User.get_many_users_by_ids([x for x in role_assignments])
        else:
            users = User.search(search_term)
            role_assignments = Role.get_role_assignments_for_users(users, roles)

        result = {'users': [], 'roles': []}
        for user in users:
            print(user.username)
            result['users'].append({
                'id': user.id,
                'name': user.username,
                'roles': role_assignments[user.id]
            })

        result['roles'] = [{'id': x.id, 'name': x.name} for x in roles]

        return result

    def save_roles(self, request):
        for user in request['users']:
            for role in user['roles']:
                user_mdl = User.find(user_id=user['id'])
                if role['state'] is True:
                    user_mdl.add_to_role(role_id=role['id'])
                else:
                    user_mdl.remove_from_role(role_id=role['id'])
        return {'success': True}

