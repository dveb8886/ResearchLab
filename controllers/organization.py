from model.organization import Organization
from model.profile import Profile

class OrganizationController():

    def __init__(self):
        pass


    def index(self):
        orgs = Organization.list()
        return list(orgs)

    def renderOrg(self, org_id):
        profs = Profile.list(org_id)
        org = Organization.find(org_id)
        return org, list(profs)

    def addOrg(self, org_name):
        org = Organization.add(org_name)
        return org
