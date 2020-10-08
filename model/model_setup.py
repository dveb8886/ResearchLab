import pugsql
import general.settings as settings
from model.organization import Organization
from model.user import User
from model.profile import Profile
from model.fund import Fund
from model.role import Role

def init():
    handler = pugsql.module('assets/sql')
    handler.connect('sqlite:///memory')
    settings.sql = handler

    # Create table if they don't exist
    handler.org_create()
    handler.user_create()
    handler.prof_create()
    handler.fund_create()
    handler.stat_create()
    handler.value_create()
    handler.role_create()
    handler.role_user_create()

    # Add test rows if they don't exist
    org = handler.org_find(id=1)
    if (org == None):
        org = Organization.add('Test Company')
        admin = User.add('admin', 'test123')
        guest = User.add('guest', 'test123')
        admin_role = Role.add('admin')
        admin.add_to_role(role_id=admin_role.id)
        profile = Profile.add('Test Profile', org.id)
        fund = Fund.add('Test Fund', 'Test Manager', 2000, 0.00, 0.00, profile.id)

    # return the queries handler
    return handler