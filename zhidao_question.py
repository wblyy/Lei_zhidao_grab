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


def get_timestamp(timestr):
    newtime = timestr
    timeArray = time.strptime(newtime, "%Y%m%d")
    #转换为时间戳:
    timeStamp = int(time.mktime(timeArray))
    return str(timeStamp)+'000'

def get_time(timestamp):
    timestamp = timestamp[:-3]
    tobj = time.localtime(int(timestamp))
    timestr = time.strftime("%Y-%m-%d %H:%M:%S", tobj)
    return timestr

def questions(tag,pn,rn):
    apiurl = 'http://wapiknow.baidu.com/mapi/question/v6/tagquestion?&tag={0}&pn={1}&rn={2}&from=new&tagAll=0&isView=1&baseTime={3}'
    tagstr = urllib.quote(tag)
    #timestamp = get_timestamp(btime)
    timestamp = str(int(time.time())) + '000'
    url = apiurl.format(tagstr,pn,rn,timestamp)

    pageinfo = getPage(url)
    try:
        pagejson = json.loads(pageinfo)
        data = pagejson.get('data')
        if data:
            qlist = data.get('list',list())
            for index,item in enumerate(qlist):
                qid = item.get('qid')
                uid = item.get('uid')
                uname = item.get('uname')
                title = item.get('title')
                content = item.get('content')
                replyCount = item.get('replyCount')
                createTime = item.get('createTime')
                statId = item.get('statId')
                tags = item.get('tags',list())
                tagsstr = "/".join(tags)
                print "<"+str(index)+"> "+"|###|".join([str(qid),str(uid),uname,title,content,tagsstr,str(createTime),get_time(str(createTime)),str(statId),str(replyCount)])
    except Exception as e:
        print "Error: ",e
        return

def answers(qid,pn,rn,ctime):
    apiurl = "http://wapiknow.baidu.com/mapi/user/v8/myask?&qid={0}&pn={1}&rn={2}&createTime={3}&answerType=0&statId=5"
    url = apiurl.format(qid,pn,rn,ctime)
    pageinfo = getPage(url)
    try:
        pagejson = json.loads(pageinfo)
        data = pagejson.get('data')
        if data:
            question = data.get('question')
            if question:
                print '~'*25+"问题"+"~"*25
                print question.get("content")
                print '~'*25+'回答'+'~'*25
            answers = data.get('answers',list())
            for index,item in enumerate(answers):
                uid = item.get('uid')
                uname = item.get('uname')
                content = item.get('content')
                print "<"+str(index)+"> "+"|###|".join([str(uid),uname,content])
            print '~'*54,'\n'
    except Exception as e:
        print "Error: ",e
        return
        

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python {0} pageNum pageSize".format(sys.argv[0])
        sys.exit(1)
    pagenum = int(sys.argv[1])
    pagesize = int(sys.argv[2])
    questions('音乐',pagenum,pagesize)
    #answers('236619962',0,10,"1416992697000")
