from flask import Flask, render_template
import json
from functions import exchange_rates_request


app = Flask(__name__)


@app.route('/')
def index():
	with open('data.json') as f:
		data = json.load(f)
	exchange_rates_request(data)
	with open('data.json', 'w') as f:
		json.dump(data, f, indent = 4, sort_keys = True)
	return render_template('index.html', data=data)