#!/usr/bin/env python
#-*- encoding:utf-8 -*-

'''
do nothing
'''
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):

    def __init__(self):
        self.debug = True