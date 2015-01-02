#!/usr/bin/env python
#-*- encoding:utf-8 -*-


def topic(current_page_num, total_page_num):
    '''
    10 pagination
    '''
    current_page_num = int(current_page_num)
    total_page_num = int(total_page_num)
    if total_page_num < 12:
        return [x for x in xrange(1, total_page_num+1)]
    if current_page_num <=7:
        return [x for x in xrange(1, 11)]
    if total_page_num - current_page_num <= 7:
        return [x for x in xrange(total_page_num-9, total_page_num+1)]
    return [x for x in xrange(current_page_num-5, current_page_num+5)]

def link(current_page_num, total_page_num):
    '''
    '''
    return topic(current_page_num, total_page_num)

if __name__ == "__main__":
    for i in xrange(1,23):
        print topic(i, 21)