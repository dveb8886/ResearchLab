from flask import Blueprint, render_template, jsonify
from controllers.organization import OrganizationController

organization_api = Blueprint('organization_api', __name__)
controller = OrganizationController()

@organization_api.route('/')
def all():
    orgs = controller.index()
    return render_template('index.html', orgs=orgs)

@organization_api.route('/<org_id>')
def org(org_id):
    org, profiles = controller.renderOrg(org_id)
    return render_template('organization.html', profiles=profiles, org=org)

@organization_api.route('/add/<org_name>')
def add(org_name):
    org = controller.addOrg(org_name)
    return jsonify(org)