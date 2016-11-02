#!/bin/env python
# -*- coding: utf-8 -*-

# @Author:yixun
# @Date:2012-11-01

from bs4 import BeautifulSoup
import getopt, sys, os

def parse(htmlfile, out, deal_num_per_month):
    f = open(htmlfile, "r")
    soup = BeautifulSoup(f)
    #print(soup.prettify())
    apartments = soup.find("div", "content").find("ul", "listContent").find_all("li")
    print "apartment.len=%d"%len(apartments)
    for k, apartment in enumerate(apartments):
        #print k
        node = apartment.find("div", "title")
        #print node
        title = ""
        url = "EmptyLink"
        if node.a != None:
            title = node.a.string
            url = node.a["href"]
        else:
            title = node.span.previous_sibling
        items = title.split(" ")
        name = items[0]
        house_type = items[1]
        area = items[2]
        idx = area.find("平".decode("utf-8"))
        if idx >= 0:
            area = area[0:idx]
        houseInfo = apartment.find("div", "address").find("div", "houseInfo").span.next_sibling
        items = houseInfo.split("|")
        chaoxiang = items[0].strip()
        zhuangxiu = items[1].strip()
        dianti = items[2].strip()
        dealDate = apartment.find("div", "address").find("div", "dealDate").string
        items = dealDate.split(".")
        year_month = items[0] + "-" + items[1]
        node = apartment.find("div", "address").find("div", "totalPrice")
        total_price = ""
        if node.span != None:
            total_price = node.span.string
            if year_month not in deal_num_per_month:
                deal_num_per_month[year_month] = 1
            else:
                deal_num_per_month[year_month] += 1
        else:
            total_price = node.string
        positionInfo = apartment.find("div", "flood").find("div", "positionInfo").span.next_sibling
        items = positionInfo.split(" ")
        idx = items[0].find("(")
        louceng = ""
        height = "未知"
        if idx >= 0:
            louceng = items[0][0:idx]
            height = items[0][idx+1:len(items[0])-1]
        else:
            louceng = items[0]
        nianfen = items[1]
        qianyue = apartment.find("div", "flood").find("div", "source").string
        node = apartment.find("div", "flood").find("div", "unitPrice")
        unit_price = ""
        if node.span != None:
            unit_price = node.span.string
        else:
            unit_price = node.string
        node = apartment.find("div", "dealHouseInfo").find("span", "dealHouseTxt")
        status = "EmptyInfo"
        if node != None:
            status = node.span.string
        tp = (url, name, house_type, area, chaoxiang,zhuangxiu, dianti, year_month, dealDate, total_price, louceng, height, nianfen, qianyue, unit_price, status)
        utf8_tp = tuple([item.encode("utf-8") for item in tp])
        out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%utf8_tp)
        #out.write("%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n"%(url, name, house_type, area, chaoxiang, 
        #     zhuangxiu, dianti, year_month, date, total_price, louceng, nianfen, qianyue, unit_price, status))

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["input=", "output="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    input_dir = ""
    output_file = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif o in ("-i", "--input"):
            input_dir = a 
        elif o in ("-o", "--output"):
            output_file = a 
        else:
            print "unhandled option"
            usage()
            sys.exit(3)    
    file_list = [
        "data/aojinghuating/index.html",
        "data/aojinghuating/index.html.1",
        "data/aojinghuating/index.html.2",
    ]
    filelist = os.listdir(input_dir)
    #print filelist
    temp = []
    for f in filelist:
        idx = f.rfind('.')
        if idx < 0:
            continue
        suffix = f[idx+1:]
        seqno = 0
        try:
            seqno = int(suffix)
        except ValueError:
            pass
        #print seqno
        temp.append((seqno, f))
    temp.sort(key=lambda item : item[0])
    out = open(output_file + ".txt", "w")
    out.write("链接\t小区\t户型\t面积(平米)\t朝向\t装修\t是否电梯\t成交年月\t成交日期\t总价(万)\t楼层\t总楼层数\t建筑年份\t签约来源\t单价(元/平)\t状态\n")
    deal_num_per_month = {}
    for t in temp:
        f = os.path.join(input_dir, t[1])
        print "***** parse file: %s"%f
        parse(f, out, deal_num_per_month)
    out.close()
    print len(deal_num_per_month)
    out2 = open(output_file + "_ym.txt", "w")
    dl = [(year_month, num) for (year_month, num) in deal_num_per_month.items()]
    dl.sort(key=lambda item : item[0], reverse=True)
    for (year_month, num) in dl:
        out2.write("%s\t%d\n"%(year_month, num))
    out2.close()

