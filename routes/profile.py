from flask import Blueprint, render_template
from controllers.profile import ProfileController

profile_api = Blueprint('profile_api', __name__)
controller = ProfileController()

@profile_api.route('/<prof_id>')
def prof(prof_id):
    prof, funds = controller.renderProf(prof_id)
    return render_template('profile.html', funds=funds, prof=prof)