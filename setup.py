# coding:utf-8
#
# Copyright (c) 2013 feilong.me All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on May 4, 2013
#

import distutils.core
try:
    import setuptools
except ImportError:
    pass

version = "0.0.1"

distutils.core.setup(
    name="owl",
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
    ]
)