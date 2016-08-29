from flask import g, request
from marshmallow import Schema, fields

from backend.app import app, db
from backend.model import Session, User
from backend.routes import auth_required, dump_with_schema, load_with_schema, make_error_response
from backend.schema import SessionSchema


@app.route('/user/sessions')
@auth_required
@dump_with_schema(SessionSchema, paged=True)
def get_user_sessions():
    return g.current_user.sessions


@app.route('/user/sessions', methods=['DELETE'])
@auth_required
def delete_user_sessions():
    g.current_user.sessions.delete()
    db.session.commit()

    return ('', 204)


class CreateSessionSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


@app.route('/sessions', methods=['POST'])
@load_with_schema(CreateSessionSchema)
@dump_with_schema(SessionSchema, context={'on_create': True})
def create_session(data):
    user = User.find_by_email_or_username(data['username'])
    if not (user and user.password == data['password']):
        return make_error_response('Invalid username/password combination', 401)

    session = Session(user=user)

    # TODO can this be made more accurate?
    session.ip_address = request.remote_addr

    if request.user_agent:
        session.user_agent = request.user_agent.string
        # Denormalize user agent
        session.platform = request.user_agent.platform
        session.browser = request.user_agent.browser

    db.session.add(session)
    db.session.commit()

    return session

@app.route('/sessions/<id>', methods=['DELETE'])
@auth_required
def delete_session(id):
    session = Session.query.get(id)
    if not (session and session.user == g.current_user):
        return make_error_response('Session not found', 404)

    db.session.delete(session)
    db.session.commit()

    return ('', 204)
