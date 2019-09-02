# coding:utf-8
import logging
import sys, os
from flask import Flask
from tornado.wsgi import WSGIContainer
from tornado.options import define
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

__ROOT__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(__ROOT__, ".."))
from owl.tornado import options


class DemoCfgOptions(object):
    __base_key__ = "myroot"
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
    define("port", default=8888, help="run on the given port", type=int)
    loop = IOLoop.instance()
    xcfg = options.DynamicPatch(loop, op)
    xcfg.add_change_callback(
        "api_url", "uname", "api_port","switch", callback_handler=on_callback
    )
    logging.info("start")
    container = WSGIContainer(app)
    http_server = HTTPServer(container)
    http_server.listen(8888)
    xcfg.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
