import json


def test_get_user(client, test_user, auth_headers):
    resp = client.get('/user', headers=auth_headers)
    assert resp.status_code == 200

    data = json.loads(resp.data.decode('utf-8'))
    assert data['id'] == test_user.id

def test_update_user(client, test_user, auth_headers):
    params = {
        'password': 'password',
    }

    resp = client.patch('/user', data=json.dumps(params), headers=auth_headers)
    assert resp.status_code == 200

    data = json.loads(resp.data.decode('utf-8'))
    assert data['id'] == test_user.id
