import base64
import json
import os
import traceback
import sys

import flask
import gevent.wsgi
import pymysql


app = flask.Flask(__name__)

relationships = json.loads(base64.b64decode(os.environ["PLATFORM_RELATIONSHIPS"]))

@app.route('/')
def hello_world():
    tests = {}
    tests["mysql"] = wrap_test(test_mysql, relationships["mysql"][0])
    return json.dumps(tests)


def wrap_test(callback, *args, **kwargs):
    try:
        result = callback(*args, **kwargs)
        return {
            "status": "OK",
            "return": result,
        }
    except Exception:
        return {
            "status": "ERROR",
            "error": traceback.format_exception(*sys.exc_info())
        }


def test_mysql(instance):
    connection = pymysql.connect(
        host=instance["host"],
        user=instance["username"],
        password=instance["password"],
        db=instance["path"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

    finally:
        connection.close()


if __name__ == "__main__":
    http_server = gevent.wsgi.WSGIServer(('127.0.0.1', int(os.environ["PORT"])), app)
    http_server.serve_forever()
