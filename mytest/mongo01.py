#!/usr/bin/env python
#-*- encoding:utf-8 -*-
from tornado.ioloop import IOLoop
from tornado import gen
import motor



client = motor.MotorClient('localhost', 27017)
db = client.pastline

## 初始化counter
# db.counter.insert({"_id":"user_id", "seq":long(1)})
# db.counter.insert({"_id":"link_id", "seq":long(1)})
# db.counter.insert({"_id":"topic_id", "seq":long(1)})
# IOLoop.instance().start()

##试用
# @gen.coroutine
# def new_user_id():
#     ret = db.counter.find_and_modify(query={ "_id": "user_id" }, update={ "$inc": { "seq": long(1) }})
#     result = yield ret
#     print result
# IOLoop.current().run_sync(new_user_id)

##找出前十名的热门话题
## db.topic.find({}).sort("rank",1).skip(0).limit(1)
# @gen.coroutine
# def top_topics():
#     cursor = db.topic.find({"user_id": long(1), "status":1}).sort("_id",-1).skip(0).limit(10) # rank从大到小
#     for document in (yield cursor.to_list(length=100)): #要100个doc
#         print document
# IOLoop.current().run_sync(top_topics)

## 某topic下的按照时间顺序的第0到10个链接
#  首先是给出该topic的id，按照link id从小到大即可

## 如何添加一个user
# 先判断给出的邮箱（该字段unique）是否已经有相同，若有相同，则不注册，提醒用户该邮箱已经注册；若无相同，使用try 创建该用户，
# 若发生异常，提醒用户稍后注册（没办法，事务的原因）
# 用户名相当于昵称，可以在后期随便修改

## 如何添加一个topic
# 生成topic id，直接添加即可

## 如何找用户收藏的0到10个链接
# 收藏时间由远到近得到收藏的link的0～10个id，
# 再来一个语句找到这些link id对应的详细信息



## 如何防止sql注入
# 除了$where、eval等，其他的不会有问题，使用时候先把数据转换为指定的类型哈


## 添加一个账户
# @gen.coroutine
# def new_user():
#     user_info = {"_id":long(2),
#                  "email":"123@gmail.com",
#                  "name":"username",
#                  "password":"",
#                  "activate_code":"",
#                  "is_activated":1,
#                  "reset_code":"",
#                  }
#     ret = db.user.insert(user_info)
#     result = yield ret
#     print result
# IOLoop.current().run_sync(new_user)


## 根据用户id查询该用户
# @gen.coroutine
# def get_user():
#     user_info = {"_id":long(1),
#                  "is_actived":1,
#                  }
#     ret = db.user.find_one(user_info)
#     result = yield ret
#     print result
# IOLoop.current().run_sync(get_user)


## 插入user_id=1一个新的topic
# @gen.coroutine
# def new_topic():
#     topic_info = {"_id":long(2),
#                     "user_id":long(1),
#                     "title":"python资源",
#                     "abstract":"python资源",
#                     "create_time": "1410438184",
#                     "modify_time": "1410438184",
#                     "star_num":0,
#                     "rank":1,
#                     "status":1
#                  }
#     ret = db.topic.insert(topic_info)
#     result = yield ret
#     print result
# IOLoop.current().run_sync(new_topic)


## 插入user_id=1, topic_id=1的一个新的link
# @gen.coroutine
# def new_link():
#     link_info = {
#                     "user_id":long(1),
#                     "topic_id":long(1),
#                     "title":"滚石评选出史上最伟大的500首经典歌曲，都是115网盘",
#                     "url":"http://blog.renren.com/share/278742534/8718089259",
#                     "create_time": "1410438184",
#                     "modify_time": "1410438184",
#                     "star_num":0,
#                     "rank":1,
#                     "status":1
#                  }
#     ret = db.link.insert(link_info)
#     result = yield ret
#     print result
# IOLoop.current().run_sync(new_link)