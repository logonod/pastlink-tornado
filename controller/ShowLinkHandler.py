#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *


class ShowLinkHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        self.id_handler = ID()
        if self.debug: print "\n--- show link ---\n"

    @gen.coroutine
    def get(self, link_hashid):
        link_hashid = link_hashid.strip()
        if len(link_hashid) == 0:
            self.redirect("/explore")
            return
        link_id = long(self.id_handler.hash2int(link_hashid))
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

        ##! 登录用户是否已经收藏该link
        star_status = False #默认未收藏
        if login == True:
            ret = self.db.user_link.find_one({"user_id":user_id, "link_id":link_id})
            result = yield ret
            if result is not None:
                if self.debug: print "登录用户已经收藏该话题"
                star_status = True
        ##!获取该link_id是否存在，以及所属用户信息
        try:
            ret = self.db.link.find_one({"_id": link_id,  "status":1})
            current_link_info = yield ret  # 当前link的详细信息
            if self.debug: print "current link info:", current_link_info
            if current_link_info is None: # 该topic不存在，不显示左栏
                self.set_status(404)
                self.render("error/404.html",
                            info="该链接不存在")
                return
            ret = self.db.user.find_one({"_id": current_link_info['user_id'],  "is_activated":1})
            current_link_user_info = yield ret  # link所属于用户的详细信息
            current_link_info['topic_hashid'] = self.id_handler.int2hash(current_link_info['topic_id'])
            if self.debug: print "current link info:", current_link_info
            if self.debug: print "login:", login
            self.render("link/index.html",
                        login=login,
                        self_access=self_access,
                        current_link_hashid=link_hashid,
                        current_link_info=current_link_info,
                        current_login_user_info = current_login_user_info,
                        current_link_user_info = current_link_user_info,
                        star_status = star_status
                        )
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