#!/bin/env python
# -*- coding: utf-8 -*-

# @Author:yixun
# @Date:2012-11-01

import getopt, sys, os
import urllib2, socket
from bs4 import BeautifulSoup
import json

URL_HEAD = "http://bj.lianjia.com/chengjiao/rs"
PG_HEAD = "http://bj.lianjia.com/chengjiao/pg"

def fetch_url(url):
    print "fetch url: %s"%url
    retry_times = 0
    while retry_times < 3:
        try:
            socket.setdefaulttimeout(20)
            f=urllib2.urlopen(url).read()
            if f == None:
                retry_times += 1
                continue
            return f
        except Exception, e:
            retry_times += 1
            print "Retry %d q=%s"%(retry_times, query)
            print e
    if retry_times == 3:
        print "Failed crawler query=%s"%(query)
        sys.exit(1)
    return None

def fetch(query):
    url = URL_HEAD + query 
    totalPage = 0
    f = fetch_url(url)
    res_list = []
    if f != None:
        soup = BeautifulSoup(f)
        temp = soup.find("div", "page-box house-lst-page-box")
        items = json.loads(temp["page-data"])
        totalPage = int(items["totalPage"])
        res_list.append(f)
        for i in xrange(2, totalPage+1):
            url = PG_HEAD + str(i) + "rs" + query
            pf = fetch_url(url)
            res_list.append(pf)
    return res_list

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hq:o:", ["query=", "output="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    query = ""
    output_file = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif o in ("-q", "--query"):
            query = a 
        elif o in ("-o", "--output"):
            output_file = a 
        else:
            print "unhandled option"
            usage()
            sys.exit(3)    
    print "query=%s"%query
    fetch(query)
