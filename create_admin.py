from getpass import getpass
import sys

from webapp import create_app, db
from webapp.model import User

app = create_app()

with app.app_context():
    username = input('Input name:')

    if User.query.filter(User.username == username).count():
        print('User already exist')
        sys.exit(0)

    password1 = getpass('Input password')
    password2 = getpass('Repeat password')

    if not password1 == password2:
        print('Passwords not equal')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('User added with id={}'.format(new_user.id))