# coding:utf-8
import sys
import os
__ROOT__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(__ROOT__, ".."))
from tornado.ioloop import IOLoop
import asyncio
import logging
import tornado
import tornado.web
from tornado.options import define, options
from owl.aio import options as a_options 
from owl.tornado import options as t_options 

class DemoCfgOptions(object):
    __base_key__ = "myroot"
    '''
     # the default value is just type template,
     # if key in consul k/v, the value will override by consul
    '''
    api_url = "h"
    api_port = 0
    admin_emails = []
    uname=""


op = DemoCfgOptions()


def on_callback(key,v):
    print(key, getattr(op,key))



def main():
    xcfg = a_options.DynamicPatch(op)
    xcfg.add_change_callback("api_url", on_callback)
    xcfg.add_change_callback("api_port", on_callback)
    xcfg.add_change_callback("uname", on_callback)
    xcfg.start()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(op.uname)

def main_tornado():
    define("port", default=8888, help="run on the given port", type=int)
    loop = IOLoop.instance()
    xcfg = t_options.DynamicPatch(loop,op)
    xcfg.add_change_callback(
        "api_url", "uname", "api_port","switch", callback_handler=on_callback
    )
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    xcfg.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main_tornado()
