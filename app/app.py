import os
from collections import defaultdict

from flask import (Flask, render_template,
                   request, make_response, url_for,
                   redirect)
from flask_login import (LoginManager, login_user,
                         login_required, current_user,
                         logout_user)
from flask_bcrypt import Bcrypt
from sqlalchemy.inspection import inspect
import pandas as pd

from db_models import db, User, UserStartups
from model import Recommender
from utils import load_stored_ids, table_to_dict, get_columns_info


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =\
    os.path.join(os.path.dirname(__file__), 'database')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =\
    os.path.join('sqlite:///',
                 'database', 'database.sqlite')
app.config['SECRET_KEY'] = "392391=24"

db.app = app
db.init_app(app)
db.create_all()
db.session.commit()

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
recommender = Recommender(app.config['UPLOAD_FOLDER'])


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


@app.route('/login', methods=["GET", "POST"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.

    """
    if request.method == 'POST':
        user = User.query.get(request.form['name'])
        if user:
            if bcrypt.check_password_hash(user.password,
                                          request.form['password']):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)

        return redirect(url_for('home'))

    else:
        return render_template('login.html')


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()

    return render_template('login.html')


@app.route('/_check')
def healthcheck():
    return 'OK'


@app.route('/')
@login_required
def home():
    return render_template('home.html',
                           companies=recommender.companies)


@app.route('/', methods=["POST"])
@login_required
def process():

    company_name = request.form['searchBar']
    threshold = request.form['similarityThresh']
    filters = request.form.getlist('filter')
    threshold = int(threshold) / 100

    if company_name is None or company_name.strip() == "":
        return redirect(url_for('home'))

    stored_data =\
        UserStartups.query.filter_by(user_name=current_user.name).all()
    saved_entries, discarded_entries =\
        load_stored_ids(stored_data)

    most_similar_companies, sorted_features =\
        recommender.find_most_similar(
            company_name,
            restricted_ids=saved_entries.union(discarded_entries),
            threshold=threshold,
            filters=filters
        )

    most_similar_companies = most_similar_companies[get_columns_info()['limited_output']]
    output = table_to_dict(most_similar_companies, sorted_features)
    response =\
        make_response(render_template('table.html', query=company_name, table=output,
                      companies=recommender.companies))
    response.set_cookie('last_query', company_name)

    return response


@app.route('/store', methods=["POST"])
@login_required
def store_entry():
    data = request.json
    entries = [entry.strip() for entry in data.split('\n') if entry.strip()]
    option = entries[-1]
    entry_id = entries[0]

    discarded = True
    if option.lower().strip() == 'save for later':
        discarded = False

    entry =\
        UserStartups(startup_id=entry_id, user_name=current_user.name,
                     is_discarded=discarded, related_query=request.cookies.get('last_query'))
    db.session.add(entry)
    db.session.commit()

    return "200"


@app.route('/display_users', methods=["GET", "POST"])
@login_required
def display_users():

    def query_to_dict(rset):
        result = defaultdict(list)
        for obj in rset:
            instance = inspect(obj)
            for key, x in instance.attrs.items():
                result[key].append(x.value)
        return result

    all_users = UserStartups.query.all()
    query_dict = query_to_dict(all_users)
    df = pd.DataFrame(query_dict)
    output = table_to_dict(df)

    return render_template('table.html', table=output,
                           companies=recommender.companies,
                           hide_options=True)


@app.route('/storedforlater', methods=["GET", "POST"])
@login_required
def display_stored():

    stored_data = UserStartups.query.filter_by(user_name=current_user.name).all()
    saved_ids, _ = load_stored_ids(stored_data)
    data = recommender.data[recommender.data['ID'].isin(saved_ids)]

    if request.method == "GET":
        output = table_to_dict(data)
        return render_template('table.html', table=output,
                               companies=recommender.companies,
                               hide_options=True,
                               download_csv=True)

    resp = make_response(data.to_csv(index=False))
    resp.headers["Content-Disposition"] =\
        "attachment; filename=recommender_export.csv"
    resp.headers["Content-Type"] = "text/csv"

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
