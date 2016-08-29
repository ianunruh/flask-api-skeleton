import json
import uuid

import pytest

from backend.app import app, db
from backend.model import Session, User

@pytest.fixture(scope='module')
def client():
    client = app.test_client()
    client.testing = True
    return client

@pytest.fixture(scope='module')
def test_user():
    username = 'testuser-%s' % str(uuid.uuid4())
    email = 'test@example.com'
    password = 'password'

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, email=email)
        user.change_password(password)
        db.session.add(user)
        db.session.commit()

    yield user

    db.session.delete(user)
    db.session.commit()

@pytest.fixture(scope='module')
def session(client, test_user):
    params = {
        'username': test_user.username,
        'password': 'password',
    }

    resp = client.post('/sessions', data=json.dumps(params))
    assert resp.status_code == 200

    data = json.loads(resp.data.decode('utf-8'))
    assert data['token']

    yield data

    # Clean up session
    Session.query.filter_by(token=data['token']).delete()

@pytest.fixture(scope='module')
def auth_headers(session):
    return {
        'X-Auth-Token': session['token'],
    }
