#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import time


class StarLinkHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        self.id_handler = ID()
        if self.debug: print "\n--- star link ---\n"

    @gen.coroutine
    def get(self):
        self.write("Hello world!")

    @gen.coroutine
    def post(self):
        link_hashid = self.get_argument("link_hashid", "").strip()
        if self.debug: print "link hashid:", link_hashid
        if link_hashid == "":
            self.write({"success": False, "info": "请先指定链接"})
            return

        action = self.get_argument("action", "")
        if action != "star" and action != "unstar":
            self.write({"success": False, "info": "没有指定正确的动作"})
            return

        link_id = long(self.id_handler.hash2int(link_hashid))

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
        ##！用户登录，查看该用户是否已经star这个link
        has_stared = False
        try:
            ret = self.db.user_link.find_one({"user_id": user_id, "link_id": link_id})
            result = yield ret
            if result is not None:
                has_stared = True
        except Exception, e:
            if self.debug: print "出现异常(2)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return

        ##！删除link
        if self.debug: print "是否已经收藏：", has_stared
        if self.debug: print "action：", action
        try:
            if has_stared == True and action == "unstar":
                ret = self.db.user_link.remove({"link_id": link_id, "user_id": user_id})
                yield ret
                ret = self.db.link.update({"_id": link_id},
                                       {"$inc":{"star_num":-1}},
                                       upsert=False)
                yield ret
                self.write({"success": True, "redirect":""})
                return
            if has_stared == False and action == "star":
                ret = self.db.user_link.insert(
                    {"link_id": link_id, "user_id": user_id, "create_time": time.time()}
                )
                yield ret
                ret = self.db.link.update({"_id": link_id},
                       {"$inc":{"star_num":1}},
                       upsert=False)
                yield ret
                self.write({"success": True, "redirect":""})
                return
        except Exception, e:
            if self.debug: print "出现异常(3)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return

        self.write({"success": False, "info":"发生错误，请稍后再试！"})