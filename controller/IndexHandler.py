#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *


class IndexHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False

    @gen.coroutine
    def get(self):
        user_id = self.get_secure_cookie("user_id")
        if self.debug: print "user_id:", user_id
        if user_id is not None:
            self.redirect("/explore")
            return
        self.render("index.html")
        return

    @gen.coroutine
    def post(self):
        self.write("Hello world!")