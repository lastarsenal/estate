#!/bin/env python
# -*- coding: utf-8 -*-

# @Author:yixun
# @Date:2012-11-01

import getopt, sys, os
import lj_crawler, lj_parser

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
    res_list = lj_crawler.fetch(query)
    out = open(output_file + ".txt", "w")
    out.write("链接\t小区\t户型\t面积(平米)\t朝向\t装修\t是否电梯\t成交年月\t成交日期\t总价(万)\t楼层\t总楼层数\t建筑年份\t签约来源\t单价(元/平)\t状态\n")
    deal_num_per_month = {}
    for f in res_list:
        lj_parser.parse(f, out, deal_num_per_month)
    out.close()
    print len(deal_num_per_month)
    out2 = open(output_file + "_ym.txt", "w")
    dl = [(year_month, num) for (year_month, num) in deal_num_per_month.items()]
    dl.sort(key=lambda item : item[0], reverse=True)
    for (year_month, num) in dl:
        out2.write("%s\t%d\n"%(year_month, num))
    out2.close()
