#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import motor


def get_conn():
    client = motor.MotorClient('localhost', 27017)
    db = motor.MotorClient('mongodb://username:password@localhost:27017/pastlink').pastlink
    return db
