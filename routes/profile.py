from flask import Blueprint, render_template, request, url_for, redirect
from controllers.profile import ProfileController

profile_api = Blueprint('profile_api', __name__)
controller = ProfileController()

@profile_api.route('/<prof_id>')
def prof(prof_id):
    prof, funds = controller.renderProf(prof_id)
    return render_template('profile.html', funds=funds, prof=prof)

@profile_api.route('/add', methods=['post'])
def add():
    prof_name = request.form['prof_name']
    org_id = request.form['org_id']
    controller.addProf(prof_name, org_id)
    return redirect(url_for('organization_api.org', org_id=org_id))
