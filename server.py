import os

import flask
import gevent.wsgi


app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


http_server = gevent.wsgi.WSGIServer(('127.0.0.1', int(os.environ["PORT"])), app)
http_server.serve_forever()
