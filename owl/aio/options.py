# coding:utf-8

import asyncio
import os
import logging
import json

import consul.aio
from consul.base import Timeout

from .. import Base

class DynamicPatch(Base):
    _conn_ = None
    _loop_ = None

    def __init__(self, cfg, consul_host="127.0.0.1", consul_port=8500):
        self._loop_ = asyncio.get_event_loop()
        self._conn_ = consul.aio.Consul(port=consul_port, loop=self._loop_)
        self.cfg = cfg
        self._loop_.create_task(self.init())

    def start(self):
        self._loop_.run_forever()
        self._loop_.close()

    @asyncio.coroutine
    def init(self):
        self._type_dict_ = {
            k: type(v) for k, v in self.cfg.__class__.__dict__.items() if k[:1] != "_"
        }
        _, data = yield from self._conn_.kv.get(self.cfg.__base_key__, recurse=True)
        if isinstance(data, list):
            self.fill_config(data)
        for key, callback_handler in self.__handers__.items():
            self._loop_.create_task(self.watch(key, callback_handler))

    @asyncio.coroutine
    def watch(self, key, callback_handler):
        index = None
        while True:
            try:
                index, data = yield from self._conn_.kv.get(
                    os.path.join(self.cfg.__base_key__, key), index=index
                )
                if data is not None:
                    if hasattr(self.cfg, key):
                        keyType = self._type_dict_[key]
                        if keyType is list or keyType is dict or keyType is bool:
                            v= json.loads(data["Value"])
                        else:
                            v = keyType(data["Value"])
                        if getattr(self.cfg, key) != v:
                            setattr(self.cfg, key, v)
                            callback_handler(key,v)
            except asyncio.TimeoutError:
                pass

