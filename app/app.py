import json
import os

from flask import (Flask, render_template,
                   request, make_response, url_for)

app = Flask(__name__)


@app.route('/_check')
def healthcheck():
    return 'OK'


@app.route('/')
def home():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
