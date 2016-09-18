from builtins import super

from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from six.moves.urllib.parse import urlparse, parse_qs


class CallbackHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback_result = None


class CallbackHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        parts = urlparse(self.path)
        query = parse_qs(parts.query)

        result = {}
        for k, v in query.items():
            if len(v) == 1:
                result[k] = v[0]
            elif len(v) == 0:
                result[k] = None
            else:
                result[k] = v

        self.server.callback_result = result

        self.wfile.write(b'You can close this window now')


def run_callback_app(host, port):
    httpd = CallbackHTTPServer((host, port), CallbackHTTPRequestHandler)
    httpd.handle_request()
    return httpd.callback_result
