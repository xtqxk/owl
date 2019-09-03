#coding:utf-8
version = "0.0.5"
import logging
import json
import consul

class Base(object):
    __handers__ = {}
    _type_dict_ = {}
    def __init__(self,cfg, consul_host="127.0.0.1", consul_port=8500):
        self.cfg = cfg
        self.consul_host  = consul_host
        self.consul_port  = consul_port
        self.init()

    def add_change_callback(self, *keys, callback_handler=None):
        if not keys or not callback_handler:
            return
        for key in keys:
            if key and key not in self.__handers__:
                self.__handers__[key] = callback_handler
        self.watching()
        
    def watching(self):
        pass

    def init(self):
        c = consul.Consul(self.consul_host,self.consul_port)
        cfg_items = None
        if not isinstance(self.cfg,dict):
            cfg_items = self.cfg.__class__.__dict__.items()
        else:
            cfg_items = self.cfg.items()
        self._type_dict_ = {
            k: type(v) for k, v in cfg_items if k[:1] != "_"
        }
        print(self._type_dict_)
        _, data = c.kv.get(self.cfg.__base_key__, recurse=True)
        if isinstance(data, list):
            self.fill_config(data)

    def fill_config(self,data):
        for item in data:
            r, key = item.get("Key", "").split("/", 1)
            if r != self.cfg.__base_key__:
                continue
            if key not in self._type_dict_:
                logging.debug("key:%s not define at options. passed!",key)
                continue
            if self._type_dict_[key] is None:
                continue
            keyType = self._type_dict_[key]
            if keyType is list or keyType is tuple or keyType is dict or keyType is bool:
                v= json.loads(item["Value"])
            elif keyType is str:
                v = item["Value"].decode()
            else:
                v = keyType(item["Value"])
            if isinstance(self.cfg, dict):
                self.cfg[key] = v
            else:
                setattr(self.cfg, key, v)
            logging.debug("CFG:key:%s,value:%s",key, v)