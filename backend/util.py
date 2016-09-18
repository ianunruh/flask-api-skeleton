import base64
import os


def generate_token(nbytes=32):
    raw = os.urandom(nbytes)
    return base64.urlsafe_b64encode(raw).decode('utf-8').rstrip('=')
