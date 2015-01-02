#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import time

class NewTopicHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        if self.debug: print "\n---/new/topic---\n"

    @gen.coroutine
    def get(self):
        user_id = self.get_secure_cookie("user_id")
        if self.debug: print "user_id:", user_id
        if user_id is None:
            self.redirect("/explore")
            return
        try:
            user_id = long(user_id)
        except:
            self.redirect("/explore")
            return
        try:
            ret = self.db.user.find_one({ "_id": user_id,  "is_activated":1})
            current_login_user_info = yield ret
            if self.debug: print "current login user info:", current_login_user_info
            if current_login_user_info is None:
                self.redirect("/explore")
                return
            self.render("new/topic.html",
                        current_login_user_info=current_login_user_info)
            return
        except Exception, e:
            if self.debug: print "出现异常：", e
            self.redirect("/explore")
            return

    @gen.coroutine
    def post(self):
        user_id = self.get_secure_cookie("user_id")
        if self.debug: print "user_id:", user_id
        if user_id is None:
            self.write({"success": False, "info": "您还没登录，请先登录！"})
            return
        try:
            user_id = long(user_id)
        except:
            self.write({"success": False, "info": "您还没登录，请先登录！"})
            return

        title = self.get_argument("title", "").strip()
        abstract = self.get_argument("abstract", "").strip()
        top_status = self.get_argument("top_status", "0").strip()

        if len(title) == 0:
            self.write({"success": False, "info": "标题不能为空。"})
            return

        try:
            top_status = int(top_status)
        except:
            top_status = 0

        ##！用户信息
        try:
            ret = self.db.user.find_one({ "_id": user_id,  "is_activated":1})
            current_login_user_info = yield ret
            if self.debug: print "current login user info:", current_login_user_info
            if current_login_user_info is None:
                self.write({"success": False, "info": "您还没登录，请先登录！"})
                return
        except:
            self.write({"success": False, "info": "系统错误，请稍后再试！"})
            return

        ##！创建话题
        try:
            ret = self.db.counter.find_and_modify(query={ "_id": "topic_id" }, update={ "$inc": { "seq": long(1) }})
            doc = yield ret
            topic_id = doc["seq"]
            if self.debug: print "新的topic id", topic_id
            create_time = time.time()
            new_topic = {
                "_id": long(topic_id),
                "user_id":user_id,
                "title":title,
                "abstract":abstract,
                "create_time":create_time,
                "modify_time":create_time,
                "status":1,
                "star_num":0,
                "rank":0.0,
                "top_status":top_status
            }
            if self.debug: print "插入新的话题：", new_topic
            yield self.db.topic.insert(new_topic) ## 持久话新话题
            self.write({"success": True, "redirect":"/u/"+current_login_user_info['name']})
            return
        except:
            self.write({"success": False, "info": "系统错误，请稍后再试！"})
            return