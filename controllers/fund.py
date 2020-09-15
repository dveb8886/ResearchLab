from model.organization import Organization
from model.profile import Profile
from model.fund import Fund
from model.stat import Stat
import general.settings as settings
import math


x_values = [1,2,3,4,5,6]
beta_values = [1.26,2.34,1.26,1.26,1.26,1.26]
alpha_values = [0,0,0,0,0,0]
rm_values = [0.06,0.04,0.19,0.16,0.08,0.09]
rf_values = [0.01,0.01,0.01,0.015,0.005,0.005]
c_values = [0.2, 0.2, 0.2, 0.15, 0.15, 0.15]
d_values = [0.1, 0.1, 0.1, 0.12, 0.15, 0.15]


class FundController():

    def __init__(self):
        pass

    def renderFund(self, fund_id):
        fund = Fund.find(fund_id)
        profile = Profile.find(fund.prof)
        organization = Organization.find(profile.org)

        # these stats are inputs and show up in the top part of the page
        stats_beta = ['Beta']
        stats_controlled = ['Alpha', 'RM', 'RF']
        stats_curves = ['c_rate', 'd_rate']

        # these stats are calculated and show up after calc is clicked
        stats_calculated = ['growth_rate', 'NAV', 'Unfunded', 'Called', 'Distributed']


        stats = {}
        x = None
        for stat_name in stats_beta+stats_controlled+stats_curves+stats_calculated:
            stat = Stat.find_by_name(stat_name, fund_id, 'db')

            if not stat == None:
                stats[stat_name] = {
                    'y': stat.get_values()[1],
                    # 'color_line': stat.color_line,
                    # 'color_fill': stat.color_fill
                    'color_line': settings.colors[stat_name]['color_line'],
                    'color_fill': settings.colors[stat_name]['color_fill']
                }
                if x == None:
                    x = stat.get_values()[0]

            elif stat_name in stats_controlled+stats_beta+stats_curves:
                stats[stat_name] = {
                    'y': [1 for x in range(6)],
                    'color_line': settings.colors[stat_name]['color_line'],
                    'color_fill': settings.colors[stat_name]['color_fill']
                }
                if x == None:
                    x = [x for x in range(6)]


        return {
            'fund_name': fund.fund_name,
            'fund': fund_id,
            'prof_name': profile.prof_name,
            'org_name': organization.org_name,
            'x': x,
            'stats': stats,
            'stats_beta': stats_beta,
            'stats_curves': stats_curves,
            'stats_controlled': stats_controlled,
            'stats_calculated': stats_calculated
        }

    # This function creates a new fund with default stats
    def addFund(self, fund_name, org_id):
        print("adding new fund")
        fund = Fund.add(fund_name, org_id)
        x = x_values

        stat_beta = Stat.add('Beta', fund.id)
        stat_beta.set_values([x, beta_values])
        stat_beta.commit_values()

        stat_alpha = Stat.add('Alpha', fund.id)
        stat_alpha.set_values([x, alpha_values])
        stat_alpha.commit_values()

        stat_rm = Stat.add('RM', fund.id)
        stat_rm.set_values([x, rm_values])
        stat_rm.commit_values()

        stat_rf = Stat.add('RF', fund.id)
        stat_rf.set_values([x, rf_values])
        stat_rf.commit_values()

        stat_c_rate = Stat.add('c_rate', fund.id)
        stat_c_rate.set_values([x, c_values])
        stat_c_rate.commit_values()

        stat_d_rate = Stat.add('d_rate', fund.id)
        stat_d_rate.set_values([x, d_values])
        stat_d_rate.commit_values()

        print("finished adding fund")
        return fund

    # this function runs when the "Calculate" button is pressed on the UI.
    # sample dataset = {fund: #, x: [x1, x2], stats:{'Red':{y:[y1, y2]}, 'Blue':{y:[y1, y2]}}}
    # expected return =  {fund: #, x: [x1, x2], stats:{
    #                       'Cyan':  {y:[y1, y2], color_line:'rgba(#, #, #, #)', color_fill:'rgba(#, #, #, #)'},
    #                       'Purple':{y:[y1, y2], color_line:'rgba(#, #, #, #)', color_fill:'rgba(#, #, #, #)'},
    #                       'Orange':{y:[y1, y2], color_line:'rgba(#, #, #, #)', color_fill:'rgba(#, #, #, #)'}
    #                    }}
    def calcGraph(self, dataset):
        x = dataset['x']
        fund = dataset['fund']

        growth_rate = []
        NAV_beginning = 100
        NAV = []
        Unfunded_beginning = 200
        Unfunded = []

        Called = []
        Distributed =[]

        for i in range (len(x)):
            growth_rate_quarterly = (dataset['stats']['Alpha']['y'][i] + dataset['stats']['RF']['y'][i] + dataset['stats']['Beta']['y'][i]*(dataset['stats']['RM']['y'][i]-dataset['stats']['RF']['y'][i]) )
            growth_rate.append(growth_rate_quarterly)

            Called_quarter = Unfunded_beginning * dataset['stats']['c_rate']['y'][i]
            Unfunded_beginning -= Called_quarter
            Unfunded.append(Unfunded_beginning)

            Called.append(Called_quarter)

            Distributed_quarter = NAV_beginning * dataset['stats']['d_rate']['y'][i]

            Distributed.append(Distributed_quarter)

            NAV_beginning *= math.exp(growth_rate_quarterly)
            NAV_beginning += (Called_quarter-Distributed_quarter)*math.exp(growth_rate_quarterly)

            NAV.append(NAV_beginning)


        return {'fund': fund, 'x': x, 'stats':{
            'growth_rate':  {'y': growth_rate,  'color_line': settings.colors['growth_rate']['color_line'], 'color_fill':   settings.colors['growth_rate']['color_fill']},
            'NAV':          {'y': NAV,          'color_line': settings.colors['NAV']['color_line'], 'color_fill':           settings.colors['NAV']['color_fill']},
            'Unfunded':     {'y': Unfunded,     'color_line': settings.colors['Unfunded']['color_line'], 'color_fill':      settings.colors['Unfunded']['color_fill']},
            'Called':       {'y': Called,       'color_line': settings.colors['Called']['color_line'], 'color_fill':        settings.colors['Called']['color_fill']},
            'Distributed':  {'y': Distributed,  'color_line': settings.colors['Distributed']['color_line'], 'color_fill':   settings.colors['Distributed']['color_fill']},

        }}

    # this function runs when the "Commit" button is pressed on the UI
    # dataset = {fund: #, x:[x1, x2], stats:{
    #               'Red'   :{y:[y1, y2]},
    #               'Blue'  :{y:[y1, y2]},
    #               'Cyan'  :{y:[y1, y2]},
    #               'Purple':{y:[y1, y2]},
    #               'Orange':{y:[y1, y2]}
    # }}
    def commitGraph(self, dataset):
        x = dataset['x']
        fund = dataset['fund']
        stats_json = dataset['stats']
        for stat_name, stat_values in stats_json.items():
            stat = Stat.find_by_name(stat_name, fund, [x, stat_values['y']])
            if stat == None: # create the stat in the database if it doesn't exist
                stat = Stat.add(stat_name, fund)
                stat.set_values([x, stat_values['y']])
                stat.color_line = settings.colors[stat_name]['color_line']
                stat.color_fill = settings.colors[stat_name]['color_fill']
            stat.commit()
            stat.commit_values()
        return 'success'