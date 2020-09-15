import pugsql
import general.settings as settings

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

    # Add test rows if they don't exist
    org = handler.org_find(id=1)
    if (org == None):
        handler.org_add(org_name='Test Company')
        handler.user_add(id=1, user_name='Test User', org=1)
        handler.prof_add(id=1, prof_name='Test Profile', org=1)
        handler.fund_add(id=1, fund_name='Test Fund', fund_manager="Test Manager", fund_vintage=2000, fund_nav=0.00, fund_unfunded=0.00, prof=1)

    # return the queries handler
    return handler