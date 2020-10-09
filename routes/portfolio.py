from flask import Blueprint, render_template, request, url_for, redirect
from controllers.portfolio import PortfolioController

portfolio_api = Blueprint('portfolio_api', __name__)
controller = PortfolioController()

@portfolio_api.route('/<portfolio_id>')
def portfolio(portfolio_id):
    portfolio, data = controller.renderPortfolio(portfolio_id)
    return render_template('portfolio.html', data=data, prof=portfolio)

@portfolio_api.route('/add', methods=['post'])
def add():
    portfolio_name = request.form['portfolio_name']
    org_id = request.form['org_id']
    controller.addPortfolio(portfolio_name, org_id)
    return redirect(url_for('organization_api.org', org_id=org_id))
