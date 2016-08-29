from flask import g

from backend.app import app, db
from backend.routes import auth_required, dump_with_schema, load_with_schema
from backend.schema import UserSchema


@app.route('/user')
@auth_required
@dump_with_schema(UserSchema)
def get_user():
    return g.current_user


@app.route('/user', methods=['PATCH'])
@auth_required
@load_with_schema(UserSchema)
@dump_with_schema(UserSchema)
def update_user(data):
    user = g.current_user

    if data['password']:
        user.change_password(data['password'])

    db.session.commit()

    return user
