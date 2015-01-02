#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from hashids import Hashids

class ID(object):
    def __init__(self):
        self.hashids = Hashids(salt='!@sasSD092f0Hu7&', min_length=6)

    def int2hash(self, id):
        return self.hashids.encrypt(long(id))

    def hash2int(self, hash_id):
        return self.hashids.decrypt(hash_id)[0]


if __name__ == "__main__":
    my = ID()
    print my.int2hash(123)
    print my.hash2int('P5Y')
