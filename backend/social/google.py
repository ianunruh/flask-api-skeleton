from datetime import datetime, timedelta

import requests
from six.moves.urllib.parse import urlencode

from backend.social.base import BaseProvider
from backend.util import generate_token

OAUTH_DIALOG_URL = 'https://accounts.google.com/o/oauth2/v2/auth?{}'
ACCESS_TOKEN_URL = 'https://www.googleapis.com/oauth2/v4/token'


class GoogleProvider(BaseProvider):
    key = 'google'

    def __init__(self, config):
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']

    def build_login_url(self, redirect_uri, state=None, scope='email'):
        if not state:
            state = generate_token()

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'state': state,
        }

        if scope:
            params['scope'] = scope

        login_url = OAUTH_DIALOG_URL.format(urlencode(params))

        return login_url, state

    def get_access_token(self, code, redirect_uri, state):
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        resp = requests.post(ACCESS_TOKEN_URL,
                             params=params,
                             headers={'Accept': 'application/json'})
        token = resp.json()

        return {
            'access_token': token['access_token'],
            'expires_at': (datetime.utcnow() + timedelta(seconds=token['expires_in'])),
        }
