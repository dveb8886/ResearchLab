import sys
import json
sys.path.insert(0, 'controllers')

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import arithmeticController

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add/<a>/<b>')
def add(a, b):
    answer = arithmeticController.add(a, b)
    return render_template('add.html', a=a, b=b, answer=answer)

@app.route('/graph')
def graph():
    return render_template('chart.html')

@app.route('/graph/calc', methods=["POST"])
def graph_calc():
    # print(request.data)
    # print(request.json)
    # print(request.form)
    # print(request)
    return jsonify(arithmeticController.calc_graph(request.json))