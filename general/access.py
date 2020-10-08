from flask_login import current_user
from flask import g
from miracle import Acl
import functools
from flask import render_template

def acl_resource(resource=None, permission=None, grants=None):
    def _decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            g.acl = gen_acl()
            acl_resource_name = resource.format(**kwargs)
            g.acl.add_permission(acl_resource_name, permission)
            for grant in grants:
                role_name = grant.format(resource=acl_resource_name)
                g.acl.add_role(role_name)
                g.acl.grant(role_name, acl_resource_name, permission)

            roles = current_user.list_roles()
            roles_unwrapped = [x.name for x in roles]

            if not g.acl.check_any(roles_unwrapped, acl_resource_name, permission):
                return render_template('403.html')

            return func(*args, **kwargs)

        return wrapper
    return _decorator

def gen_acl():
    acl = Acl()
    acl.add_resource('admin_menu')
    acl.add_permission('admin_menu', 'view')
    acl.add_role('admin')
    acl.grant('admin', 'admin_menu', 'view')
    return acl

