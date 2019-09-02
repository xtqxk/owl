# coding:utf-8
import sys
import os

__ROOT__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(__ROOT__, ".."))
from flask import Flask
from gevent import pywsgi as wsgi
import logging
from owl.gevent import options


class DemoCfgOptions(object):
    __base_key__ = "myroot"  # consul k/v folder
    """
     # the default value is just type template,
     # if key in consul k/v, the value will override by consul
    """
    api_url = "h"
    api_port = 0
    admin_emails = []
    uname = ""
    switch = True


op = DemoCfgOptions()


def on_callback(key, v):
    print(key, getattr(op, key))


app = Flask(__name__)


@app.route("/")
def index():
    return op.uname


def main():
    xcfg = options.DynamicPatch(op)
    xcfg.add_change_callback(
        "api_url", "api_port", "uname", "switch", callback_handler=on_callback
    )
    xcfg.start()
    server = wsgi.WSGIServer(("127.0.0.1", 8888), app)
    server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
