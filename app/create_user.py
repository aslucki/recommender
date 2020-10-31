#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys

from app import app, db, bcrypt
from db_models import User


def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            create = input("Create a new user? y/n \n")
            if create == 'n':
                return

        name = input("name: ")
        password = getpass()
        assert password == getpass('Password (again): ')

        user = User(
            name=name,
            password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    sys.exit(main())
