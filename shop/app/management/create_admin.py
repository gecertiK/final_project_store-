from datetime import datetime

from flask_security import hash_password

from app.models import Role, User, roles_users_table
from app.utils.security import user_datastore
from db import db

color = lambda x, y, z: ";".join([str(x), str(y), str(z)])

red = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 31, 40), x)
yellow = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 33, 40), x)
green = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 32, 40), x)
cyan = lambda x: '\x1b[%sm%s\x1b[0m' % (color(6, 36, 40), x)

to_date = lambda x: datetime.strptime(x[:x.rfind('.')], '%Y-%m-%d %H:%M:%S')


def create_admin(username='admin', email='admin', password='admin'):
    username = username if username else 'admin'
    email = email if email else 'admin@noreply.com'
    password = password if password else 'admin'
    print(cyan('Inserting \'Role\' tuples'))
    if not Role.query.filter(Role.name == 'admin').first():
        user_datastore.create_role(
            name='admin',
            permissions='admin',
            description='admin'
        )
        try:
            db.session.commit()
            print(green(f'admin-role: added.'), end=' ')
        except:
            print(red(f'admin-role: error.'), end=' ')
    else:
        print(yellow(f'admin-role: exists.'), end=' ')
    print()

    print(cyan('Inserting \'User\' tuples'))
    if not User.query.filter(User.username == username).first():
        user_datastore.create_user(
            username=username,
            email=email,
            password=hash_password(password))
        try:
            db.session.commit()
            print(green(f'user-admin: added.'), end=' ')
        except:
            print(red(f'user-admin: error.'), end=' ')
    else:
        print(yellow(f'user-admin: exists.'), end=' ')
    print()

    rb = roles_users_table.insert().values(**{'user_id': User.query.filter(User.username == 'admin').first().id,
                                              'role_id': Role.query.filter(Role.name == 'admin').first().id})
    # try:
    role = Role.query.filter(Role.name == 'admin').first()
    user = User.query.filter(User.username == 'admin').first()

    if not user.has_role(role):
        try:
            db.session.execute(rb)
            db.session.commit()
            print(green(f'user-admin: admin-role added.'), end=' ')
        except:
            print(red(f'user-admin: admin-role error.'), end=' ')
    else:
        print(yellow(f'user-admin: admin-role exists.'), end=' ')

