#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys,os
import demjson
import time
import json
import socket
import urllib
import urllib2
from random import choice

reload(sys)
sys.setdefaultencoding("utf8")

socket.setdefaulttimeout(120)

def warning(text):
    return '\033[93m' + text + '\033[0m'

def error(text):
    return '\033[91m' + text + '\033[0m'

def other(text):
    return '\033[92m' + text + '\033[0m'


USER_AGENTS = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko) Safari/419.3',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'
]

def getPage(url, referer=''):
    response = ''
    for i in range(3):
        request = urllib2.Request(url)
        request.add_header("User-Agent", choice(USER_AGENTS))
        if referer:
            request.add_header("Refeer", referer)
        try:
            response = urllib2.urlopen(request)
            if response:
                result = response.read()
                response.close()
                return result
        except Exception as e:
            if response:
                response.close()
    return ''



def get_question(pn,rn):
    apiurl = 'http://wapiknow.baidu.com/mbrowse/ajax/getQl?cids=%5B99%5D&lm=2&pn={0}&rn={1}'
    url = apiurl.format(pn,rn)

    pageinfo = getPage(url)
    try:
        pagejson = json.loads(pageinfo)
        data = pagejson.get('data')
        if not data:
            print error("Get Nothing!! ")
            return 
        questions = data.get('questions')
        if questions:
            qlist = questions.get('entry',list())
            
            print warning("| <index> | qid | uid | uname | title | content | class_name | createTime | timestr | replyCount |")
            print warning("~"*120)
            for index,item in enumerate(qlist):
                qid = item.get('qid')
                uid = item.get('uid')
                uname = item.get('uname')
                title = item.get('title')
                content = item.get('content')
                replyCount = item.get('reply_count')
                createTime = item.get('create_time')
                timestr = item.get('time')
                class_name = item.get('class_name')
                print other("<"+str(index)+">"),
                print other("|###|".join([str(qid),str(uid),uname,title,content,class_name,str(createTime),timestr,str(replyCount)]))
                print other("URL:"),'http://zhidao.baidu.com/question/{0}.html'.format(qid)
                print 
            print warning("~"*120)
    except Exception as e:
        print "Error: ",e
        return

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python {0} pageNum pageSize".format(sys.argv[0])
        sys.exit(1)
    pagenum = int(sys.argv[1])
    pagesize = int(sys.argv[2])
    get_question(pagenum,pagesize)
