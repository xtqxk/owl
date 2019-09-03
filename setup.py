#!/usr/bin/env python
# coding:utf-8
#
# Copyright (c) 2019 xtqxk All rights reserved.
#
# @author: XTQXK <xtqxk.kilroy@gmail.com>
# Created on SEP 2, 2019
#

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

version = "0.0.5"

setup(
    name="consul-owl",
    version=version,
    packages=["owl", "owl.aio", "owl.gevent","owl.tornado"],
    author="XTQXK",
    author_email="xtqxk.kilroy@gmail.com",
    url="https://github.com/xtqxk/owl",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Owl is a python Consul config center for Tornado, Gevent, Flask and AioHTTP",
    install_requires=[
        "python-consul",
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)