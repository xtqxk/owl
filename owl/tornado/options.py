# coding:utf-8
import os
import logging
import json

from tornado.gen import coroutine
from consul.base import Timeout
from consul.tornado import Consul

from .. import Base


class DynamicPatch(Base):
    _conn_ = None
    _loop_ = None

    def __init__(self, loop, cfg, consul_host="127.0.0.1", consul_port=8500):
        super().__init__(cfg,consul_host=consul_host, consul_port=consul_port)
        self._loop_ = loop
        self._conn_ = Consul(port=consul_port, host=consul_host)
        self._loop_.add_callback(self.watching)

    def start(self):
        self._loop_.start()

    @coroutine
    def watching(self):
        cfg_items = None
        if not isinstance(self.cfg,dict):
            cfg_items = self.cfg.__class__.__dict__.items()
        else:
            cfg_items = self.cfg.items()
        self._type_dict_ = {
            k: type(v) for k, v in cfg_items if k[:1] != "_"
        }
        _, data = yield self._conn_.kv.get(self.cfg.__base_key__, recurse=True)
        if isinstance(data, list):
            self.fill_config(data)

        for key, callback_handler in self.__handers__.items():
            self._loop_.add_callback(self.watch, key, callback_handler)

    @coroutine
    def watch(self, key, callback_handler):
        index = None
        while True:
            try:
                index, data = yield self._conn_.kv.get(
                    os.path.join(self.cfg.__base_key__, key), index=index
                )
                if data is not None:
                    if hasattr(self.cfg, key):
                        keyType = self._type_dict_[key]
                        if keyType is list or keyType is dict or keyType is bool:
                            v = json.loads(data["Value"])
                        else:
                            v = keyType(data["Value"])
                        if getattr(self.cfg, key) != v:
                            setattr(self.cfg, key, v)
                            callback_handler(key, v)
            except Timeout:
                pass

