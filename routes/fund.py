from flask import Blueprint, render_template, request, jsonify
from controllers.fund import FundController

fund_api = Blueprint('fund_api', __name__)
controller = FundController()

@fund_api.route('/<fund_id>')
def fund(fund_id):
    answers = controller.renderFund(fund_id)
    return render_template('fund.html',
           fund_name=answers['fund_name'],
           prof_name=answers['prof_name'],
           org_name=answers['org_name']
    )

@fund_api.route('/calc', methods=["POST"])
def graph_calc():
    return jsonify(controller.calcGraph(request.json))