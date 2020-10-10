import json
import os

import pandas as pd
from flask import (Flask, render_template,
                   request, make_response, url_for)

from model import Recommender

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =\
    os.path.join(os.path.dirname(__file__), 'database')

recommender = Recommender(app.config['UPLOAD_FOLDER'])


@app.route('/_check')
def healthcheck():
    return 'OK'


@app.route('/')
def home():
    return render_template('home.html',
                           companies=recommender.companies)


@app.route('/', methods=["POST"])
def process():
    company_name = request.form["searchBar"]
    most_similar_companies = recommender.find_most_similar(company_name)
    output = table_to_dict(most_similar_companies)
    return render_template('table.html', query=company_name, table=output,
                           companies=recommender.companies)


@app.route('/companies')
def show_available_data():
    output = table_to_dict(recommender.data)
    return render_template('table.html', table=output,
                           companies=recommender.companies)


def table_to_dict(table: pd.DataFrame):

    columns = table.columns
    rows = table.values
    details = "test description of differences and similarities"
    return {"columns": columns, "rows": rows, "details": details}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
