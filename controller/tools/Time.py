#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import time

def timestamp2date(timestamp):
    timestamp = float(timestamp)
    x = time.localtime(timestamp)  # 例如1317091800 -> 2011-09-27
    return time.strftime('%Y-%m-%d', x)

if __name__ == "__main__":
    print timestamp2date(0);
