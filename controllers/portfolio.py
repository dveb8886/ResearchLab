from model.profile import Profile
from model.fund import Fund

class PortfolioController():

    def __init__(self):
        pass

    def renderPortfolio(self, portfolio_id):
        portfolio = Profile.find(portfolio_id)
        funds = Fund.list(portfolio_id)
        return portfolio, list(funds)

    def addPortfolio(self, prof_name, org_id):
        prof = Profile.add(prof_name, org_id)
        return prof