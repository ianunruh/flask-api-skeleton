import json


def test_create_session_by_email(client, test_user):
    params = {
        'username': test_user.email,
        'password': 'password',
    }

    resp = client.post('/sessions', data=json.dumps(params))
    assert resp.status_code == 200

    data = json.loads(resp.data.decode('utf-8'))
    assert data['token']


def test_create_session_by_username(client, test_user):
    params = {
        'username': test_user.username,
        'password': 'password',
    }

    resp = client.post('/sessions', data=json.dumps(params))
    assert resp.status_code == 200

    data = json.loads(resp.data.decode('utf-8'))
    assert data['token']


def test_create_session_bad_password(client, test_user):
    params = {
        'username': test_user.username,
        'password': 'notmypassword'
    }

    resp = client.post('/sessions', data=json.dumps(params))
    assert resp.status_code == 401


def test_create_session_bad_username(client):
    params = {
        'username': 'noway',
        'password': 'notmypassword'
    }

    resp = client.post('/sessions', data=json.dumps(params))
    assert resp.status_code == 401


def test_delete_session(client, test_user):
    params = {
        'username': test_user.username,
        'password': 'password',
    }

    resp = client.post('/sessions', data=json.dumps(params))
    assert resp.status_code == 200

    data = json.loads(resp.data.decode('utf-8'))
    assert data['token']

    headers = {
        'X-Auth-Token': data['token'],
    }

    resp = client.delete('/sessions/%s' % data['id'], headers=headers)
    assert resp.status_code == 204

def test_delete_user_sessions(client, test_user, auth_headers):
    resp = client.delete('/user/sessions', headers=auth_headers)
    assert resp.status_code == 204

    resp = client.delete('/user/sessions', headers=auth_headers)
    assert resp.status_code == 401
