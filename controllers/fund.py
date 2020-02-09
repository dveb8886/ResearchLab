from model.organization import Organization
from model.profile import Profile
from model.fund import Fund

class FundController():

    def __init__(self):
        pass

    def renderFund(self, fund_id):
        fund = Fund.find(fund_id)
        profile = Profile.find(fund.prof)
        organization = Organization.find(profile.org)

        return {
            'fund_name': fund.fund_name,
            'prof_name': profile.prof_name,
            'org_name': organization.org_name
        }

    def calcGraph(self, dataset):
        redTotal = 0
        red = []
        blueTotal = 0
        blue = []
        cyanTotal = 0
        cyan = []

        for i in range (len(dataset[0])):
            redTotal += dataset[0][i]
            red.append(redTotal)
            blueTotal += dataset[1][i]
            blue.append(blueTotal)
            cyanTotal += (dataset[0][i] + dataset[1][i])
            cyan.append(cyanTotal)

        return [red, blue, cyan]