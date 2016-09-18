#!/usr/bin/env python
from backend.app import app, manager
from backend.social import social_provider_registry
from backend.testutils.oauth2 import run_callback_app

@manager.command
def test_social_provider(key):
    provider_cls = social_provider_registry.get(key)

    if not provider_cls:
        print('ERROR: Social provider is unknown:', key)
        return

    provider = provider_cls(app.config['SOCIAL_PROVIDERS'][key])

    redirect_uri = 'http://localhost:5050/callback'

    login_url, state = provider.build_login_url(redirect_uri)

    print('Visit the following URL in your browser:', login_url)

    result = run_callback_app('localhost', 5050)

    if state != result['state']:
        print('ERROR: CSRF token mismatch: expected "%s"; actual "%s"' % (state, result['state']))
        return

    token = provider.get_access_token(result['code'], redirect_uri, state)
    print(token)


manager.run()
