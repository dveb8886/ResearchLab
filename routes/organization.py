from flask import Blueprint, render_template, request, redirect, url_for
from controllers.organization import OrganizationController
from flask_login import login_required
from general.access import acl_resource

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
    return render_template('organization.html', profiles=profiles, org=org)



@organization_api.route('/add', methods=['post'])
def add():
    org_name = request.form['org_name']
    controller.addOrg(org_name)
    return redirect(url_for('organization_api.all'))

