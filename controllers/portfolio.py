from model.profile import Profile
from model.fund import Fund
from model.stat import Stat
from controllers.fund import FundController
import general.settings as settings
import numpy as np

fund_controller = FundController()

class PortfolioController():

    def __init__(self):
        pass

    def renderPortfolio(self, portfolio_id):
        portfolio = Profile.find(portfolio_id)
        funds = Fund.list(portfolio_id)

        stats_names = ['Beta', 'Alpha', 'RM', 'RF', 'c_rate', 'd_rate']

        data = {
            'funds': [],
            'portfolio': portfolio_id
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

    def calcGraph(self, dataset):

        subTotalNav = []
        subTotalUnfunded = []
        subTotalCalled = []
        subTotalDistributed = []

        finalStat = {}
        funds = []

        for fund_id in dataset['funds']:
            subTotalStat = fund_controller.calcGraph(dataset['funds'][fund_id], fund_id)
            subTotalNav.append(subTotalStat['stats']['NAV'])
            subTotalUnfunded.append(subTotalStat['stats']['Unfunded'])
            subTotalCalled.append(subTotalStat['stats']['Called'])
            subTotalDistributed.append(subTotalStat['stats']['Distributed'])

            funds.append({
                'fund_id': fund_id,
                'stats': {
                    'NAV': {'y': subTotalStat['stats']['NAV'], 'color_line': settings.colors['NAV']['color_line'],
                            'color_fill': settings.colors['NAV']['color_fill']},
                    'Unfunded': {'y': subTotalStat['stats']['Unfunded'], 'color_line': settings.colors['Unfunded']['color_line'],
                                 'color_fill': settings.colors['Unfunded']['color_fill']},
                    'Called': {'y': subTotalStat['stats']['Called'], 'color_line': settings.colors['Called']['color_line'],
                               'color_fill': settings.colors['Called']['color_fill']},
                    'Distributed': {'y': subTotalStat['stats']['Distributed'],
                                    'color_line': settings.colors['Distributed']['color_line'],
                                    'color_fill': settings.colors['Distributed']['color_fill']}
                }
            })

        finalStat['NAV'] = np.sum(subTotalNav, axis=0).tolist()
        finalStat['Unfunded'] = np.sum(subTotalUnfunded, axis=0).tolist()
        finalStat['Called'] = np.sum(subTotalCalled, axis=0).tolist()
        finalStat['Distributed'] = np.sum(subTotalDistributed, axis=0).tolist()

        return {'x': 6, 'funds': funds, 'stats': {
            'NAV': {'y': finalStat['NAV'],                 'color_line': settings.colors['NAV']['color_line'],         'color_fill': settings.colors['NAV']['color_fill']},
            'Unfunded': {'y': finalStat['Unfunded'],       'color_line': settings.colors['Unfunded']['color_line'],    'color_fill': settings.colors['Unfunded']['color_fill']},
            'Called': {'y': finalStat['Called'],           'color_line': settings.colors['Called']['color_line'],      'color_fill': settings.colors['Called']['color_fill']},
            'Distributed': {'y': finalStat['Distributed'], 'color_line': settings.colors['Distributed']['color_line'], 'color_fill': settings.colors['Distributed']['color_fill']},
        }}