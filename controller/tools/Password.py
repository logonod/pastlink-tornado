#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import base64, hashlib


def encrypt(plaintext):
    '''
     encrypt plaintext
    '''
    plaintext = str(plaintext) + 'lmnopq'
    encoded = base64.b64encode(plaintext)
    return hashlib.sha256(encoded).hexdigest()


if __name__ == '__main__':
    # print encrypt('')
    print encrypt('123456')
