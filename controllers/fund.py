from model.organization import Organization
from model.profile import Profile
from model.fund import Fund
from model.stat import Stat
import general.settings as settings

class FundController():

    def __init__(self):
        pass

    def renderFund(self, fund_id):
        fund = Fund.find(fund_id)
        profile = Profile.find(fund.prof)
        organization = Organization.find(profile.org)
        stats_controlled = ['Red', 'Blue'] # these stats show up in the top graph
        stats_calculated = ['Cyan', 'Purple', 'Orange'] # these stats show up in the bottom graph

        stats = {}
        x = None
        for stat_name in stats_controlled+stats_calculated:
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
            elif stat_name in stats_controlled:
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
            'stats_controlled': stats_controlled
        }

    # This function creates a new fund with default stats
    def addFund(self, fund_name, fund_manager, fund_vintage, fund_nav, fund_unfunded, prof):
        fund = Fund.add(fund_name, fund_manager, fund_vintage, fund_nav, fund_unfunded, prof)
        x = [1,2,3,4,5,6]
        stat_red = Stat.add('Red', fund.id)
        stat_red.set_values([x, [1,1,1,1,1,1]])
        stat_red.commit_values()
        stat_blue = Stat.add('Blue', fund.id)
        stat_blue.set_values([x, [1,1,1,1,1,1]])
        stat_blue.commit_values()
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
        fund_db = Fund.find(fund)
        nav_value = fund_db.fund_nav
        unfunded_valuev = fund_db.fund_unfunded
        fund_manager = fund_db.fund_manager
        vintage_value = fund_db.fund_vintage

        cyanTotal = 0
        cyan = []
        purpleTotal = 0
        purple = []
        orangeTotal = 0
        orange = []

        for i in range (len(x)):
            purpleTotal += dataset['stats']['Red']['y'][i]
            purple.append(purpleTotal)
            orangeTotal += dataset['stats']['Blue']['y'][i]
            orange.append(orangeTotal)
            cyanTotal += (dataset['stats']['Red']['y'][i] + dataset['stats']['Blue']['y'][i])
            cyan.append(cyanTotal)

        return {'fund': fund, 'x': x, 'stats':{
            'Cyan': {'y':cyan, 'color_line': settings.colors['Cyan']['color_line'], 'color_fill': settings.colors['Cyan']['color_fill']},
            'Purple': {'y':purple, 'color_line': settings.colors['Purple']['color_line'], 'color_fill': settings.colors['Purple']['color_fill']},
            'Orange': {'y':orange, 'color_line': settings.colors['Orange']['color_line'], 'color_fill': settings.colors['Orange']['color_fill']}
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