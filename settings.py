#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sae.const

settings = { 
    "static_path" : os.path.join(os.path.dirname(__file__), "static"), 
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "cookie_secret" : "JVixFqkpQ9i8gdDJb3Zx0i/Wos5aqUZKtnDCM2mecFc=",
    "debug":True,
}


saedb = {
    "host": sae.const.MYSQL_HOST,
    "db": sae.const.MYSQL_DB,
    "port": sae.const.MYSQL_PORT,
    "user": sae.const.MYSQL_USER,
    "password": sae.const.MYSQL_PASS,
}