import os

import pandas as pd
from flask import (Flask, render_template,
                   request, make_response, url_for)

from model import Recommender
from utils import load_stored_ids, table_to_dict

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
    saved_entries, discarded_entries = load_stored_ids(app.config['UPLOAD_FOLDER'])

    company_name = request.form["searchBar"]
    most_similar_companies, sorted_features =\
        recommender.find_most_similar(
            company_name,
            restricted_ids=saved_entries.union(discarded_entries))
    output = table_to_dict(most_similar_companies, sorted_features)

    return render_template('table.html', query=company_name, table=output,
                           companies=recommender.companies)


@app.route('/store', methods=["POST"])
def store_entry():
    data = request.json
    entries = [entry.strip() for entry in data.split('\n') if entry.strip()]
    option = entries[-1]
    entry_id = entries[0]

    if option.lower().strip() == 'save for later':
        path = os.path.join(app.config['UPLOAD_FOLDER'],
                            'saved_entries.txt')
    else:
        path = os.path.join(app.config['UPLOAD_FOLDER'],
                            'discarded_entries.txt')

    with open(path, 'a') as f:
        f.write(entry_id + '\n')

    return "200"


@app.route('/companies')
def show_available_data():
    output = table_to_dict(recommender.data)
    return render_template('table.html', table=output,
                           companies=recommender.companies)


@app.route('/savedforlater')
def display_stored():
    saved_ids, _ = load_stored_ids(app.config['UPLOAD_FOLDER'])
    output =\
        table_to_dict(recommender.data[recommender.data['ID'].isin(saved_ids)])
    return render_template('table.html', table=output,
                           companies=recommender.companies, hide_options=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
