#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import math

class UserHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        self.id_handler = ID()
        if self.debug: print "\n---UserHandler---\n"

    @gen.coroutine
    def get(self, username=""):
        username = username.strip()  # url中给出的用户名
        if self.debug: print "url中的用户名：", username
        ##! 是否在url中给出username。例如/u/letian，若没给出，则跳转到/login
        if len(username) == 0:
            #todo
            self.redirect("/login")
            return
        ##!url中给出的用户是否存在
        try:
            ret = self.db.user.find_one({ "name": username,  "is_activated":1})
            query_user_info = yield ret
            if query_user_info is None: # url中的用户不存在
                if self.debug: print "没有用户：", username
                #todo
                self.redirect("/login")
                return
        except:
            self.redirect("/login")
            return

        ##!是否有用户登录
        login = False        #已经登录
        self_access = False  #自己访问自己
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
                    if username == current_login__user_info['name']:
                        self_access = True
            except Exception, e:
                if self.debug: print "出现异常(1)：", e
                pass
        ##!tab 和 page
        tab = self.get_argument("tab", "topic").strip()
        page = self.get_argument("page", "1").strip()
        try:
            page = int(page)
        except:
            page = 1
        if self.debug: print "page:", page

        ##! tab = topic
        if tab == "topic":
            try:
                ret = self.db.topic.find({"user_id": query_user_info['_id']}).count(True)
                topic_sum = yield ret
                if self.debug: print "the number of %s's topic: %d" %(query_user_info['name'], topic_sum)
                pages_sum = math.ceil(topic_sum/10.0)
                current_page_num = page
                if current_page_num > pages_sum:
                    current_page_num = pages_sum
                pagination = Pagination.topic(current_page_num, pages_sum)
                if self.debug: print "paginatin:", pagination
                start = current_page_num*10 -10
                if start < 0 : start = 0
                ret = self.db.topic.find({"user_id": query_user_info['_id'], "status":1}).\
                    sort([("top_status", -1),("_id",-1)]).skip(start).limit(10)
                topics = []
                for doc in (yield ret.to_list(length=10)):
                    doc["hashid"] = self.id_handler.int2hash(doc["_id"])
                    doc["create_date"] = Time.timestamp2date(doc["create_time"])
                    topics.append(doc)
                if self.debug: print "topics:", topics
                self.render("user/index.html",
                            login=login,
                            self_access=self_access,
                            current_login_user_info = current_login__user_info,
                            query_user_info = query_user_info,
                            current_page_num = current_page_num,
                            pagination = pagination,
                            topics = topics,
                            success = True)
                return
            except Exception,e:
                if self.debug: print "出现异常：", e
                self.render("user/index.html",
                            query_user_info = query_user_info,
                            current_login_user_info = current_login__user_info,
                            login=login,
                            self_access = self_access,
                            success = False)
                return

        ##! tab = topic-stars
        if tab == "topic-stars":
            try:
                ret = self.db.user_topic.find({"user_id": query_user_info['_id']}).count(True)
                topic_sum = yield ret
                if self.debug: print "the number of %s's starred topic : %d" %(query_user_info['name'], topic_sum)
                pages_sum = math.ceil(topic_sum/10.0)
                current_page_num = page
                if current_page_num > pages_sum:
                    current_page_num = pages_sum
                pagination = Pagination.topic(current_page_num, pages_sum)
                if self.debug: print "paginatin:", pagination
                start = current_page_num*10 -10
                if start < 0 : start = 0

                ret = self.db.user_topic.find({"user_id": query_user_info['_id']}).\
                    sort([("create_time", -1)]).skip(start).limit(10)
                topics = []
                for doc in (yield ret.to_list(length=10)):
                    try:
                        topic_id = doc['topic_id']
                        ret2 = self.db.topic.find_one({"_id": topic_id})
                        topic = yield ret2
                        topic["hashid"] = self.id_handler.int2hash(topic["_id"])
                        topic["create_date"] = Time.timestamp2date(topic["create_time"])
                        topics.append(topic)
                    except:
                        pass
                if self.debug: print "topics:", topics
                self.render("user/topic-stars.html",
                            login=login,
                            self_access=self_access,
                            current_login_user_info = current_login__user_info,
                            query_user_info = query_user_info,
                            current_page_num = current_page_num,
                            pagination = pagination,
                            topics = topics,
                            success = True)
                return
            except Exception,e:
                if self.debug: print "出现异常：", e
                self.render("user/index.html",
                            query_user_info = query_user_info,
                            current_login_user_info = current_login__user_info,
                            login=login,
                            self_access = self_access,
                            success = False)
                return

        ##! tab = link-stars
        if tab == "link-stars":
            try:
                ret = self.db.user_link.find({"user_id": query_user_info['_id']}).count(True)
                link_sum = yield ret
                if self.debug: print "the number of %s's starred link : %d" %(query_user_info['name'], link_sum)
                pages_sum = math.ceil(link_sum/10.0)
                current_page_num = page
                if current_page_num > pages_sum:
                    current_page_num = pages_sum
                pagination = Pagination.topic(current_page_num, pages_sum)
                if self.debug: print "paginatin:", pagination
                start = current_page_num*10 -10
                if start < 0 : start = 0

                ret = self.db.user_link.find({"user_id": query_user_info['_id']}).\
                    sort([("create_time", -1)]).skip(start).limit(10)
                links = []
                for doc in (yield ret.to_list(length=10)):
                    try:
                        link_id = doc['link_id']
                        ret2 = self.db.link.find_one({"_id": link_id})
                        link = yield ret2
                        link["hashid"] = self.id_handler.int2hash(link["_id"])
                        link["create_date"] = Time.timestamp2date(link["create_time"])
                        links.append(link)
                    except:
                        pass
                if self.debug: print "links:", links
                self.render("user/link-stars.html",
                            login=login,
                            self_access=self_access,
                            current_login_user_info = current_login__user_info,
                            query_user_info = query_user_info,
                            current_page_num = current_page_num,
                            pagination = pagination,
                            links = links,
                            success = True)
                return
            except Exception,e:
                if self.debug: print "出现异常：", e
                self.render("user/index.html",
                            query_user_info = query_user_info,
                            current_login_user_info = current_login__user_info,
                            login=login,
                            self_access = self_access,
                            success = False)
                return



        self.render("user.html", login = False)

    @gen.coroutine
    def post(self):
        self.write("Hello world!")