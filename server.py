import importlib
import general.settings as settings
from general.access import gen_acl
import model.model_setup as model_setup
from routes.organization import organization_api
from routes.portfolio import portfolio_api
from routes.profile import profile_api
from routes.fund import fund_api
from routes.account import account_api
from flask_login import LoginManager, current_user
from model.user import User
from miracle import Acl


from flask import Flask, g
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
login = LoginManager(app)
login.login_view = 'account_api.login'

# initialize settings and model
settings.init()
model_setup.init()

@app.context_processor
def include_in_template():
    return {
        'acl': g.acl if 'acl' in g else gen_acl(),
        'current_user': current_user,
        'roles': [x.name for x in current_user.list_roles()] if not current_user.is_anonymous else []
    }

# register user loader function for login purposes
@login.user_loader
def user_loader(id):
    return User.find(id)

# initialize major routes and their controllers
# these routes can be found in the routes/ directory
app.register_blueprint(account_api, url_prefix='/account')
app.register_blueprint(organization_api, url_prefix='/organization')
app.register_blueprint(portfolio_api, url_prefix='/portfolio')
app.register_blueprint(profile_api, url_prefix='/profile')
app.register_blueprint(fund_api, url_prefix='/fund')

# This route is used to arbitrarily run model commands for testing purposes
# it will turn a command like 'GET /model/profile/add/profileName,1' into ...
# model.profile.Profile.add('profileName', 1) .. which will add the profile into organization 1
@app.route('/model/<table>/<method>/<params>')
def model(table, method, params):
    mod = importlib.import_module("model."+table.lower())
    tbl = getattr(mod, table.capitalize())
    met = getattr(tbl, method)
    return str(met(*params.split(',')))