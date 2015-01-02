#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *


class ExploreHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        # self.db = self.settings['db']
        self.id_handler = ID()
        if self.debug: print "\n---ExploreHandler---\n"

    @gen.coroutine
    def get(self):

        ##!是否有用户登录
        login = False        #已经登录
        current_login__user_info = {}
        user_id = self.get_secure_cookie("user_id")
        if self.debug: print "cookie中的user_id：", user_id
        if user_id is not None:  ## 有用户登录
            try:
                user_id = long(user_id)
                ret = self.db.user.find_one({ "_id": user_id,  "is_activated":1})
                current_login__user_info = yield ret
                if self.debug: print "current login user info:", current_login__user_info
                if current_login__user_info is not None: # 有用户登录
                    login = True
            except Exception, e:
                if self.debug: print "出现异常(1)：", e
                pass

        hot_topics = []
        try:
            ret = self.db.topic.find({"status":1}).sort([("rank", -1)]).skip(0).limit(10)
            for doc in (yield ret.to_list(length=10)):
                doc["hashid"] = self.id_handler.int2hash(doc["_id"])
                hot_topics.append(doc)
        except:
            pass

        new_topics = []
        try:
            ret = self.db.topic.find({"status":1}).sort([("create_time", -1)]).skip(0).limit(10)
            for doc in (yield ret.to_list(length=10)):
                doc["hashid"] = self.id_handler.int2hash(doc["_id"])
                new_topics.append(doc)
        except:
            pass


        hot_links = []
        try:
            ret = self.db.link.find({"status":1}).sort([("rank", -1)]).skip(0).limit(10)
            for doc in (yield ret.to_list(length=10)):
                doc["hashid"] = self.id_handler.int2hash(doc["_id"])
                hot_links.append(doc)
        except:
            pass

        new_links = []
        try:
            ret = self.db.link.find({"status":1}).sort([("create_time", -1)]).skip(0).limit(10)
            for doc in (yield ret.to_list(length=10)):
                doc["hashid"] = self.id_handler.int2hash(doc["_id"])
                new_links.append(doc)
        except:
            pass

        self.render("explore.html",
                    login=login,
                    current_login_user_info = current_login__user_info,
                    hot_topics = hot_topics,
                    new_topics = new_topics,
                    hot_links = hot_links,
                    new_links = new_links)

    @gen.coroutine
    def post(self):
        self.write("Hello world!")