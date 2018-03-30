import server as httpd
import os
import sys

class AsyncWSGIServer(httpd.AsyncServer):

    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


class AsyncWSGIRequestHandler(httpd.AsyncHTTPRequestHandler):

    def get_environ(self):
        env = {}
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = sys.stdin
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False

        return env

    def start_response(self, status, response_headers, exc_info=None):
        self.response_code, self.response_message = status.split(" ")[:2]
        self.send_response(self.response_code, self.response_message)

        for key, value in response_headers:
            self.send_header(key, value)

        self.end_headers()    

    def handle_request(self):
        env = self.get_environ()
        app = server.get_app()
        result = app(env, self.start_response)
        self.finish_response(result)

    def finish_response(self, result):
        self.send(bytes(self.response.encode('utf-8')) + result)
        self.close()


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return b'Hello World'

server = AsyncWSGIServer(handler_class=AsyncWSGIRequestHandler)
server.set_app(application)
server.serve_forever()