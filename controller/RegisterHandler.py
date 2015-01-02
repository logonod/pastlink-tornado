#!/usr/bin/env python
#-*- encoding:utf-8 -*-


from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import time

class RegisterHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        pass

    @gen.coroutine
    def get(self):
        self.render("register.html")