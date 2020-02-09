import importlib
import general.settings as settings
import model.model_setup as model_setup
from routes.organization import organization_api
from routes.profile import profile_api
from routes.fund import fund_api

from flask import Flask
app = Flask(__name__)

# initialize settings and model
settings.init()
model_setup.init()

# initialize major routes and their controllers
# these routes can be found in the routes/ directory
app.register_blueprint(organization_api, url_prefix='/organization')
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