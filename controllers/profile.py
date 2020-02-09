from model.profile import Profile
from model.fund import Fund

class ProfileController():

    def __init__(self):
        pass

    def renderProf(self, prof_id):
        prof = Profile.find(prof_id)
        funds = Fund.list(prof_id)
        return prof, list(funds)

    def addProf(self, prof_name, org_id):
        prof = Profile.add(prof_name, org_id)
        return prof