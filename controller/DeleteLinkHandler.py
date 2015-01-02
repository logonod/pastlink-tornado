#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler
from tornado import gen
from tools import *


class DeleteLinkHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        self.id_handler = ID()
        if self.debug: print "\n--- delete link ---\n"

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
        ##！用户登录，查看是否是这个用户的link
        try:
            ret = self.db.link.find_one({ "_id": link_id, "user_id": user_id})
            current_link_info = yield ret
            if current_link_info is None:
                self.write({"success": False, "info": "该链接不属于当前用户"})
                return
        except Exception, e:
            if self.debug: print "出现异常(2)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return


        ##！删除link
        try:
            ret = self.db.link.remove({"_id": link_id, "user_id": user_id})
            yield ret
            ret = self.db.user_link.remove({"link_id": link_id})
            yield ret
            if self.debug: print "成功成功"
            self.write({"success": True, "redirect":""})
            return
        except Exception, e:
            if self.debug: print "出现异常(3)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return




        self.write({"success": False, "info":"小错误"})