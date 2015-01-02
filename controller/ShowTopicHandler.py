#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import math


class ShowTopicHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        self.id_handler = ID()
        if self.debug: print "\n--- show topic ---\n"

    @gen.coroutine
    def get(self, topic_hashid):
        topic_hashid = topic_hashid.strip()
        if len(topic_hashid) == 0:
            self.redirect("/explore")
            return
        topic_id = long(self.id_handler.hash2int(topic_hashid))
        ##!是否有用户登录
        login = False        #已经登录
        self_access = False  #自己访问自己
        current_login_user_info = {}
        user_id = self.get_secure_cookie("user_id")
        if self.debug: print "cookie中的user_id：", user_id
        if user_id is not None:  ## 有用户登录
            try:
                user_id = long(user_id)
                ret = self.db.user.find_one({ "_id": user_id,  "is_activated":1})
                current_login_user_info = yield ret
                if self.debug: print "current login user info:", current_login_user_info
                if current_login_user_info is not None: # 有用户登录
                    login = True
            except Exception, e:
                if self.debug: print "出现异常(1)：", e
                pass
        ##!获取该topic_id是否存在，以及所属用户信息
        try:
            ret = self.db.topic.find_one({"_id": topic_id,  "status":1})
            current_topic_info = yield ret  # 当前topic的详细信息
            if self.debug: print "current topic info:", current_topic_info
            if current_topic_info is None: # 该topic不存在，不显示左栏
                self.set_status(404)
                self.render("error/404.html",
                            info="该话题不存在")
                return

            ret = self.db.user.find_one({"_id": current_topic_info['user_id'],  "is_activated":1})
            current_topic_user_info = yield ret  # topic所属于用户的详细信息
            if self.debug: print "current_topic_user_info:", current_topic_user_info
            if self.debug: print "current_login_user_info:", current_login_user_info
            if current_login_user_info is None:
                self.render("error/system.html",
                            info="抱歉，系统错误，请刷新重试！")
                return
            try:
                if current_login_user_info['name'] == current_topic_user_info['name']:
                    self_access = True
            except:
                pass

            ##! 登录用户是否已经收藏该topic
            star_status = False #默认未收藏
            if login == True:
                ret = self.db.user_topic.find_one({"user_id":user_id, "topic_id":topic_id})
                result = yield ret
                if result is not None:
                    if self.debug: print "登录用户已经收藏该话题"
                    star_status = True


            if self.debug: print "star_status:", star_status
            if self.debug: print "self_access:", self_access
            page = self.get_argument("page", "1")
            try:
                page = int(page)
            except:
                page = 1
            if self.debug: print "page:", page
            ret = self.db.link.find({"topic_id": topic_id, "status":1}).count(True)
            link_sum = yield ret
            pages_sum = math.ceil(link_sum/10.0)
            current_page_num = page
            if current_page_num > pages_sum:
                current_page_num = pages_sum
            pagination = Pagination.topic(current_page_num, pages_sum)
            if self.debug: print "pagination:", pagination
            start = current_page_num*10 -10
            if start < 0 : start = 0
            ret = self.db.link.find({"topic_id": topic_id, "status":1})\
                .sort([("top_status", -1),("_id",-1)]).skip(start).limit(10)
            links = []
            for doc in (yield ret.to_list(length=10)):
                doc["hashid"] = self.id_handler.int2hash(doc["_id"])
                doc["create_date"] = Time.timestamp2date(doc["create_time"])
                links.append(doc)
            if self.debug: print "links:", links
            self.render("topic/index.html",
                        login=login,
                        self_access=self_access,
                        current_topic_info=current_topic_info,
                        current_topic_hashid = topic_hashid,
                        current_login_user_info = current_login_user_info,
                        current_topic_user_info = current_topic_user_info,
                        current_page_num = current_page_num,
                        pagination = pagination,
                        links = links,
                        success = True,
                        star_status = star_status)
            return
        except Exception, e:
            if self.debug: print "出现异常（2）：", e
            self.render("error/system.html",
                        info="抱歉，系统错误，请刷新重试！")
            return

        self.write("Hello world!")

    @gen.coroutine
    def post(self):
        self.write("Hello world!")