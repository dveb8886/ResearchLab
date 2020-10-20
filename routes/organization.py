from flask import Blueprint, render_template, request, redirect, url_for, g
from controllers.organization import OrganizationController
from flask_login import login_required, current_user
from general.access import acl_resource
from model.role import Role

organization_api = Blueprint('organization_api', __name__)
controller = OrganizationController()
test_var = {'test': 0}

@organization_api.route('/')
def all():
    orgs = controller.index()
    return render_template('index.html', orgs=orgs)


@organization_api.route('/test')
def test():
    test_var['test'] += 1
    return 'var='+str(test_var)


@organization_api.route('/<org_id>')
@login_required
@acl_resource(resource='org_{org_id}', permission='read', grants=[
    '{resource}_admin',
    '{resource}_user'
])
def org(org_id):
    org, profiles = controller.renderOrg(org_id)

    # grant permission to org admin to see admin menu
    g.acl.grant(org.get_resource()+'_admin', org.get_resource()+'_admin_menu', 'view')

    # return html
    return render_template('organization.html', profiles=profiles, org=org)



@organization_api.route('/add', methods=['post'])
def add():
    # create org
    org_name = request.form['org_name']
    org = controller.addOrg(org_name)

    # create roles and assign admin rights to creating user
    Role.add(org.get_resource()+'_admin')
    Role.add(org.get_resource()+'_user')
    current_user.add_to_role(role_name=org.get_resource()+'_admin')
    current_user.add_to_role(role_name=org.get_resource()+'_user')

    # return html
    return redirect(url_for('organization_api.all'))

