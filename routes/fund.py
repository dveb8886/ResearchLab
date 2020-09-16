from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from controllers.fund import FundController

fund_api = Blueprint('fund_api', __name__)
controller = FundController()

@fund_api.route('/<fund_id>')
def fund(fund_id):
    answers = controller.renderFund(fund_id)
    return render_template('fund.html',
                           fund_name=answers['fund_name'],
                           fund=answers['fund'],
                           prof_name=answers['prof_name'],
                           org_name=answers['org_name'],
                           x=answers['x'],
                           stats=answers['stats'],
                           stats_controlled=answers['stats_controlled']
    )

@fund_api.route('/add', methods=['post'])
def add():
    fund_name = request.form['fund_name']
    prof_id = request.form['prof_id']
    fund_manager = request.form['fund_manager']
    fund_vintage = request.form['fund_vintage']
    fund_nav = request.form['fund_nav']
    fund_unfunded = request.form['fund_unfunded']

    controller.addFund(fund_name, fund_manager, fund_vintage, fund_nav, fund_unfunded, prof_id)
    return redirect(url_for('profile_api.prof', prof_id=prof_id))

@fund_api.route('/calc', methods=["post"])
def graph_calc():
    return jsonify(controller.calcGraph(request.json))

@fund_api.route('/commit', methods=["post"])
def commit_graph():
    return jsonify(controller.commitGraph(request.json))