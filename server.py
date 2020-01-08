import sys
sys.path.insert(0, 'controllers')

from flask import Flask, render_template
app = Flask(__name__)

import arithmeticController

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add/<a>/<b>')
def add(a, b):
    answer = arithmeticController.add(a, b)
    return render_template('add.html', a=a, b=b, answer=answer)