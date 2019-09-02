#coding:utf-8
version = "0.0.1"
import logging
import json

class Base(object):
    __handers__ = {}
    _type_dict_ = {}
    def __init__(self):
        self.cfg = None
    def add_change_callback(self, *keys, callback_handler=None):
        if not keys or not callback_handler:
            return
        for key in keys:
            if key and key not in self.__handers__:
                self.__handers__[key] = callback_handler
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
            if keyType is list or keyType is dict or keyType is bool:
                v= json.loads(item["Value"])
            else:
                v = keyType(item["Value"])
            setattr(self.cfg, key, v)
            logging.debug("CFG:key:%s,value:%s",key, v)