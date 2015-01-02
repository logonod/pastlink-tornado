#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *


class LoginHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()

    @gen.coroutine
    def get(self):
        user_id = self.get_secure_cookie("user_id")
        if user_id is not None:
            ret = self.db.user.find_one({ "_id": user_id,  "is_activated":1})
            current_user_info = yield ret
            if current_user_info is not None:
                self.redirect("/u/"+current_user_info['name'])
                return
        self.render("login.html", error= False)
        return

    @gen.coroutine
    def post(self):
        email = self.get_argument("email", "").strip()
        if self.debug: print email
        password = self.get_argument("password", "").strip()
        if len(email) == 0 or len(password) == 0:
            self.write({"success": False, "info": "输入不正确，请检查。"})
            return
        password = Password.encrypt(password)
        ret = self.db.user.find_one({"email":email, "password": password, "is_activated":1})
        doc = yield ret

        if self.debug: print email, password, doc

        if doc is None:
            # print "验证失败，"
            self.write({"success": False, "info": "验证失败，请重新输入。"})
        else:
            # print "登录成功， 设置cookie"
            self.set_secure_cookie("user_id", str(doc["_id"]))
            self.write({"success": True, "redirect": "/u/"+doc["name"]})
        return