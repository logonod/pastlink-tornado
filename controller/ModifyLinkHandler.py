#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from tornado.web import RequestHandler, Application, url
from tornado import gen
from tools import *
import time


class ModifyLinkHandler(RequestHandler):

    @gen.coroutine
    def initialize(self):
        self.debug = False
        self.db = DB.get_conn()
        self.id_handler = ID()
        if self.debug: print "\n--- modify link ---\n"

    @gen.coroutine
    def get(self):
        self.write("Hello world!")

    @gen.coroutine
    def post(self):
        link_hashid = self.get_argument("link_hashid", "").strip()
        url = self.get_argument("url", "")
        title = self.get_argument("title", "").strip()
        abstract = self.get_argument("abstract", "").strip()
        if self.debug: print "link hashid:", link_hashid
        if self.debug: print "url:", url
        if self.debug: print "title:", title
        if self.debug: print "abstract:", abstract

        top_status = self.get_argument("top_status", "0")
        try:
            top_status = int(top_status)
        except:
            top_status = 0

        if link_hashid == "":
            self.write({"success": False, "info": "请先指定链接"})
            return
        if title == "" or url == "":
            self.write({"success": False, "info": "链接和标题不能为空"})
            return

        link_id = long(self.id_handler.hash2int(link_hashid))
        user_id = self.get_secure_cookie("user_id")
        if self.debug: print "link id:", link_id
        if self.debug: print "user id:", user_id
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
            if self.debug: print "current link info:", current_link_info
            if current_link_info is None:
                self.write({"success": False, "info": "该链接不属于当前用户"})
                return
        except Exception, e:
            if self.debug: print "出现异常(2)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return
        ##!检查在这个链接所属于的topic里是否已经存在这个链接
        try:
            ret = self.db.link.find_one({ "topic_id": current_link_info['topic_id'], "url":url, "_id":{"$ne":link_id}})
            result = yield ret
            if self.debug: print "新链接是否已经在topic中存在：", result
            if result is not None:
                self.write({"success": False, "info": "当前话题下已经存在该链接"})
                return
        except Exception, e:
            if self.debug: print "出现异常(a)：", e
            pass
        ##！修改link
        try:
            ret = self.db.link.update({"_id": link_id, "user_id": user_id},
                                       {"$set":{"title":title, "url": url,
                                                "abstract":abstract,
                                                "top_status":top_status,
                                                "modify_time":time.time()}},
                                       upsert=False)
            result = yield ret
            if self.debug: print "修改成功"
            self.write({"success": True, "redirect":"/topic/"+link_hashid})
            return
        except Exception, e:
            if self.debug: print "出现异常(3)：", e
            self.write({"success": False, "info": "系统错误，请稍后再试"})
            return




        self.write({"success": False, "info":"小错误"})