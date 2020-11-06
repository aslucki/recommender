from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    :param str name: name address of user
    :param str password: encrypted password for the user
    """
    __tablename__ = 'user'

    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.name

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class UserStartups(db.Model):
    """
    :param str name: name address of user
    :param str password: encrypted password for the user
    """
    __tablename__ = 'user_startups'

    entry_id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer)
    user_name = db.Column(db.String)
    is_discarded = db.Column(db.Boolean)
    related_query = db.Column(db.String)
    time = db.Column(db.DateTime)

    def __init__(self, startup_id, user_name, is_discarded, related_query):
        self.startup_id = startup_id
        self.user_name = user_name
        self.is_discarded = is_discarded
        self.related_query = related_query
        self.time = datetime.now()
