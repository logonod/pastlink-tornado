#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import time

class ProfileHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        if self.debug: print "\n---user profile---\n"

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
            self.render("profile.html",
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

        old_password = self.get_argument("old", "").strip()
        new_password = self.get_argument("new", "").strip()

        if old_password == "" or new_password == "":
            self.write({"success": False, "info": "密码不能为空。"})
            return

        if len(new_password) < 6:
            self.write({"success": False, "info": "密码不能少于6个字符。"})
            return

        ##！用户信息
        try:
            ret = self.db.user.find_one({ "_id": user_id,  "password":Password.encrypt(old_password)})
            current_login_user_info = yield ret
            if self.debug: print "current login user info:", current_login_user_info
            if current_login_user_info is None:
                self.write({"success": False, "info": "旧密码输入错误！"})
                return
        except:
            self.write({"success": False, "info": "系统错误，请稍后再试！"})
            return

        ##！修改密码
        try:
            ret = self.db.user.update({ "_id": user_id},
                                         { "$set": { "password": Password.encrypt(new_password) } },
                                         upsert=False)
            doc = yield ret
            self.write({"success": True, "redirect":"/profile"})
            return
        except:
            self.write({"success": False, "info": "系统错误，请稍后再试！"})
            return
