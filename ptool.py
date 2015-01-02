#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import pymongo
from controller.tools import *

client = pymongo.Connection('localhost', 27017)
db = client.pastlink
db.authenticate('username', 'password')

print db

## 初始化counter
def init_db():
    db.counter.insert({"_id":"user_id", "seq":long(1)})
    db.counter.insert({"_id":"link_id", "seq":long(1)})
    db.counter.insert({"_id":"topic_id", "seq":long(1)})
    db.user.ensure_index("name", unique = True)
    db.user.ensure_index("email", unique = True)

## 添加用户
def add_user():
    user_info = {"_id":long(3),
                 "email":"123@gmail.com",
                 "name":"****",
                 "password":Password.encrypt("123"),
                 "activate_code":"",
                 "is_activated":1,
                 "reset_code":"",
                 }
    ret = db.user.insert(user_info)


if __name__ == '__main__':
    pass
    add_user()
