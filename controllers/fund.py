from model.organization import Organization
from model.profile import Profile
from model.fund import Fund
from model.stat import Stat

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
                stats[stat.stat_name] = stat.get_values()[1]
                if x == None:
                    x = stat.get_values()[0]
            elif stat_name in stats_controlled:
                stats[stat_name] = [1 for x in range(6)]
                if x == None:
                    x = [x for x in range(6)]

        return {
            'fund_name': fund.fund_name,
            'fund': fund_id,
            'prof_name': profile.prof_name,
            'org_name': organization.org_name,
            'x': x,
            'y': stats,
            'stats_controlled': stats_controlled
        }

    # This function creates a new fund with default stats
    def addFund(self, fund_name, org_id):
        fund = Fund.add(fund_name, org_id)
        x = [1,2,3,4,5,6]
        stat_red = Stat.add('Red', fund.id)
        stat_red.set_values([x, [1,2,3,2,4,5]])
        stat_red.commit_values()
        stat_blue = Stat.add('Blue', fund.id)
        stat_blue.set_values([x, [5,4,3,2,1,3]])
        stat_blue.commit_values()
        return fund

    # this function runs when the "Calculate" button is pressed on the UI.
    # sample dataset = {fund: #, x: [x1, x2], y:{'Red':[y1, y2], 'Blue':[y1, y2]}}
    # expected return =  {fund: #, x: [x1, x2], y:{'Cyan':[y1, y2], 'Purple':[y1, y2], 'Orange':[y1, y2]}}
    def calcGraph(self, dataset):
        x = dataset['x']
        fund = dataset['fund']

        cyanTotal = 0
        cyan = []
        purpleTotal = 0
        purple = []
        orangeTotal = 0
        orange = []

        for i in range (len(x)):
            purpleTotal += dataset['y']['Red'][i]
            purple.append(purpleTotal)
            orangeTotal += dataset['y']['Blue'][i]
            orange.append(orangeTotal)
            cyanTotal += (dataset['y']['Red'][i] + dataset['y']['Blue'][i])
            cyan.append(cyanTotal)

        return {'fund': fund, 'x': x, 'y':{'Cyan': cyan, 'Purple': purple, 'Orange': orange}}

    # this function runs when the "Commit" button is pressed on the UI
    # dataset = {fund: #, x:[x1, x2], y:{'Red':[y1, y2], 'Blue':[y1, y2], 'Cyan':[y1, y2], 'Purple':[y1, y2], 'Orange':[y1, y2]}}
    def commitGraph(self, dataset):
        x = dataset['x']
        fund = dataset['fund']
        stats_json = dataset['y']
        for stat_name, stat_values in stats_json.items():
            stat = Stat.find_by_name(stat_name, fund, [x, stat_values])
            if stat == None: # create the stat in the database if it doesn't exist
                stat = Stat.add(stat_name, fund)
                stat.set_values([x, stat_values])
            stat.commit_values()
        return 'success'