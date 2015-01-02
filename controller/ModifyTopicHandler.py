#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import time

class ModifyTopicHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        self.id_handler = ID()
        if self.debug: print "\n--- modify topic ---\n"

    @gen.coroutine
    def get(self):
        self.write("Hello world!")

    @gen.coroutine
    def post(self):
        topic_hashid = self.get_argument("topic_hashid", "").strip()
        title = self.get_argument("title", "").strip()
        abstract = self.get_argument("abstract", "").strip()
        top_status = self.get_argument("top_status", "0")
        try:
            top_status = int(top_status)
        except:
            top_status = 0
        if self.debug: print "topic hashid:", topic_hashid
        if self.debug: print "title:", title
        if self.debug: print "abstract:", abstract
        if topic_hashid == "":
            self.write({"success": False, "info": "请先指定话题"})
            return
        if title == "":
            self.write({"success": False, "info": "标题不能为空"})
            return

        topic_id = long(self.id_handler.hash2int(topic_hashid))

        user_id = self.get_secure_cookie("user_id")
        if user_id is not None:  ## 有用户登录
            try:
                user_id = long(user_id)
                ret = self.db.user.find_one({ "_id": user_id,  "is_activated":1})
                current_login_user_info = yield ret
                if self.debug: print "current login user info:", current_login_user_info
                if current_login_user_info is  None: # 没有用户登录
                    if self.debug: print "没有用户登录"
                    self.write({"success": False, "info": "请先登录"})
                    return
            except Exception, e:
                if self.debug: print "出现异常(1)：", e
                self.write({"success": False, "info": "系统错误，请稍后再试"})
                return
        ##！用户登录，查看是否是这个用户的topic
        try:
            ret = self.db.topic.find_one({ "_id": topic_id, "user_id": user_id})
            current_topic_info = yield ret
            if current_topic_info is None:
                self.write({"success": False, "info": "该话题不属于当前用户"})
                return
        except Exception, e:
            if self.debug: print "出现异常(2)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return

        ##！修改topic
        if self.debug: print "new top status:", top_status
        try:
            ret = self.db.topic.update({"_id": topic_id, "user_id": user_id},
                                       {"$set":{"title":title, "abstract":abstract,
                                                "top_status":top_status,
                                                "modify_time":time.time()}},
                                       upsert=False)
            result = yield ret
            if self.debug: print "修改成功"
            self.write({"success": True, "redirect":"/topic/"+topic_hashid})
            return
        except Exception, e:
            if self.debug: print "出现异常(3)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return




        self.write({"success": False, "info":"小错误"})