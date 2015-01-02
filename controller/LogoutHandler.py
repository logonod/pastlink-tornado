#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *



class LogoutHandler(RequestHandler):


    @gen.coroutine
    def get(self):
        self.clear_cookie("user_id")
        self.redirect("/login")
        return

    @gen.coroutine
    def post(self):
        self.write("Hello world!")