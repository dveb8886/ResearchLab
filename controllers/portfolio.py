from model.profile import Profile
from model.fund import Fund
from model.stat import Stat

class PortfolioController():

    def __init__(self):
        pass

    def renderPortfolio(self, portfolio_id):
        portfolio = Profile.find(portfolio_id)
        funds = Fund.list(portfolio_id)

        stats_names = ['Beta', 'Alpha', 'RM', 'RF', 'c_rate', 'd_rate']

        data = {
            'funds': []
        }

        for fund in funds:
            fund_obj = {
                'id': fund.id,
                'name': fund.fund_name,
                'manager': fund.fund_manager,
                'vintage': fund.fund_vintage,
                'nav': fund.fund_nav,
                'unfunded': fund.fund_unfunded
            }

            for stat_name in stats_names:
                stat = Stat.find_by_name(stat_name, fund.id, 'db')

                if not stat == None:
                    fund_obj[stat_name] = stat.get_values()[1]
                else:
                    fund_obj[stat_name] = [0 for x in range(6)]

            data['funds'].append(fund_obj)

        return portfolio, data

    def addPortfolio(self, prof_name, org_id):
        prof = Profile.add(prof_name, org_id)
        return prof
