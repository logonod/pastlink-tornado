#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os
from tornado.ioloop import IOLoop
from tornado.web import Application, url
import controller
import motor


# db = motor.MotorClient('mongodb://username:password@localhost:27017').pastlink

# db = motor.MotorClient('mongodb://username:password@localhost:27017/pastlink').pastlink

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "MDc0NDRmYTJiZTJmZDc3ZjFkMzUwYWI4",
    "xsrf_cookies": True,
    # "db":db
}

app = Application([
                      url(r"/", controller.IndexHandler),
                      url(r"/login", controller.LoginHandler),
                      url(r"/logout", controller.LogoutHandler),
                      url(r"/explore", controller.ExploreHandler),
                      url(r"/u/(.*)", controller.UserHandler),
                      url(r"/star/link", controller.StarLinkHandler), #ajax post
                      url(r"/star/topic", controller.StarTopicHandler), #ajax post
                      url(r"/new/topic", controller.NewTopicHandler),
                      url(r"/topic/(.*)", controller.ShowTopicHandler),
                      url(r"/new/link", controller.NewLinkHandler),  #ajax post
                      url(r"/delete/topic", controller.DeleteTopicHandler),  #ajax post
                      url(r"/modify/topic", controller.ModifyTopicHandler),  #ajax post
                      url(r"/link/(.*)", controller.ShowLinkHandler),     #get -> show link
                      url(r"/delete/link", controller.DeleteLinkHandler), #ajax post
                      url(r"/modify/link", controller.ModifyLinkHandler), #ajax post
                      url(r"/profile", controller.ProfileHandler),
                      url(r"/register", controller.RegisterHandler),
                  ], **settings)
app.listen(8888)
IOLoop.current().start()
