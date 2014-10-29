import tornado.web
from tornado.httpclient import AsyncHTTPClient

from urls import urls
from settings import settings

application = tornado.web.Application(urls, **settings)