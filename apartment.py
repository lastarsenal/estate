#!/bin/env python
# -*- coding: utf-8 -*-
#filename: apartment.py

import math

"""
本程序计算根据这个网页所阐述算法写成
http://news.bj.lianjia.com/baike/018339.html
"""

LOC_IN_5_RING = 4
LOC_5_6_RING = 5
LOC_OUT_6_RING = 6

"""
普通住宅认定标准，商品房同时满足以下条件：
1. 容积率>=1.0(一般都满足)
2. 建筑面积<=140平方米
3. 每平米单价，或者房屋总价不超过最高限。
根据京建发[2014] 382号文件，对于房屋区域在五环内，五环到六环，
六环外的每平米单价和总价有不同规定，具体参考：
http://www.bjjs.gov.cn/publish/portal0/tab662/info92647.htm

同时考虑到实际执行中计算契税时要将房屋网签价格除以1.05不超过京建发[2014] 382号就按普通住宅缴纳契税，
因此这个字典中存的值是将京建发[2014] 382号乘以1.05，当做普通住宅线。这样在计算契税时不用再除以1.05判断
"""
"""
PRICE_IN_5_LIMIT = 491
PRICE_5_6_LIMIT = 393
PRICE_OUT_6_LIMIT = 294
"""
PRICE_IN_5_LIMIT = 468
PRICE_5_6_LIMIT = 374
PRICE_OUT_6_LIMIT = 280

CURRENT_CASH = 200
DEBT = 83
APARTMENT_SQ = 74.0

ORDINARY_APARTMENT_DICT = {
    LOC_IN_5_RING:PRICE_IN_5_LIMIT,
    LOC_5_6_RING:PRICE_5_6_LIMIT,
    LOC_OUT_6_RING:PRICE_OUT_6_LIMIT
}

ORDINARY_APARTMENT_DICT2 = {
    LOC_IN_5_RING:4.1580,
    LOC_5_6_RING:3.3264,
    LOC_OUT_6_RING:2.4948
}

class apartment:
    def __init__(self, desc, tp, wp, op, area, location, is_man5_uniq, is_man2 = True, is_first = True, lixi = 0.0):
        self.desc = desc
        """房屋总价"""
        self.total_price = tp
        """房屋网签价格"""   
        self.wangqian_price = wp
        """之前购入价"""
        self.original_total_price = op
        """面积"""
        self.area = area
        """房屋每平米价格"""
        self.price_per_square = self.total_price / float(self.area)
        """网签每平米价格"""
        self.wq_price_per_square = self.wangqian_price / float(self.area)
        """房屋位置，决定普住线"""
        self.location = location
        """是否满五唯一"""
        self.is_man5_uniq = is_man5_uniq 
        """房产证是否满2年，决定增值税计算"""
        self.is_man2 = is_man2
        """是否首套"""   
        self.is_first = is_first
        """业主所还利息"""   
        self.lixi = lixi
        self.zengzhishui = 0.0

    def is_ordinary_apartment(self):
        if self.area <= 140.0 and (self.wangqian_price <= ORDINARY_APARTMENT_DICT[self.location] 
                or self.wq_price_per_square <= ORDINARY_APARTMENT_DICT2[self.location]):
            return True
        return False
           
    """
    计算房屋增值税

    """
    def calc_ZengZhiShui(self):
        zengzhishui = 0.0
        if self.is_man2:
            if not self.is_ordinary_apartment():
                zengzhishui = (self.wangqian_price - self.original_total_price) / 1.05 * 0.056
        else:
            """不满2，全额征收，总价/1.05*5.6%"""
            zengzhishui = (self.wangqian_price / 1.05) * 0.056    
        return zengzhishui

    """计算契税"""            
    def calc_QiShui(self):
        qishui = 0.0
        if self.is_first:
            if self.area <= 90:
                qishui = self.wangqian_price * 0.01
            else:
                qishui = self.wangqian_price * 0.015
        else:
            qishui = self.wangqian_price * 0.03
        return qishui
     
    """
    计算个税
    TODO: 减去业主贷款所还利息
    """    
    def calc_GeShui(self):
        geshui = 0.0
        base = 0.0
        if not self.is_man5_uniq:
            base = (self.wangqian_price - self.wangqian_price * 0.1 - self.original_total_price 
                   - self.original_total_price * 0.01 - self.zengzhishui - self.lixi)
            if base > 0:
                geshui = base * 0.2
        return (geshui, base)

    def calc_ZhongJieFei(self):
        return self.total_price * 0.027

    def calc_ShouFu(self):
        shoufu = math.ceil(self.wangqian_price * 0.35)
        daikuan = self.wangqian_price - shoufu
        return (shoufu, daikuan)

    def calc_RealPay(self):
        price_gap = self.total_price - self.wangqian_price
        (shoufu, daikuan) = self.calc_ShouFu()
        real_shoufu = shoufu + price_gap
        zhongjiefei = self.calc_ZhongJieFei()
        self.zengzhishui = self.calc_ZengZhiShui()
        qishui = self.calc_QiShui()
        (geshui, base) = self.calc_GeShui()
        real_pay = real_shoufu + zhongjiefei + self.zengzhishui + qishui + geshui
        man2_display = "否"
        if self.is_man2:
            man2_display = "是"
        man5_display = "否"
        if self.is_man5_uniq:
            man5_display = "是"
        ordinary_desc = "否"
        if self.is_ordinary_apartment():
            ordinary_desc = "是"
        print "***********%s************"%self.desc
        print "房屋基本信息"
        print "\t房屋报价: %.3f万"%self.total_price
        print "\t房屋网签价: %.3f万"%self.wangqian_price
        print "\t房屋面积: %.3f平"%self.area
        print "\t报价每平米价格: %.3f万"%self.price_per_square
        print "\t网签每平米价格: %.3f万"%self.wq_price_per_square
        print "\t房屋原值: %.3f万"%self.original_total_price
        print "\t房屋位置: %d"%(self.location)
        print "\t是否满二: %s"%(man2_display)
        print "\t是否满五唯一: %s"%(man5_display)
        print "\t是否普通住宅: %s"%(ordinary_desc)
        print "实际付款信息"
        print "\t实付现金: %.3f万"%real_pay
        print "\t以下五项明细"
        print "\t首付款: %.3f万(%.3f万+%.3f万)"%(real_shoufu, shoufu, price_gap)
        print "\t中介费: %.3f万"%(zhongjiefei)
        print "\t增值税: %.3f万"%(self.zengzhishui)
        print "\t契税: %.3f万"%qishui
        print "\t个税: %.3f万"%geshui
        print "入手成本"
        cost = self.total_price + zhongjiefei + self.zengzhishui + qishui + geshui
        cost_per_square = cost / self.area
        promote = ((cost - self.total_price) / self.total_price) 
        print "\t房屋入手成本: %.3f万"%cost
        print "\t每平成本: %.3f万"%cost_per_square
        print "\t当前每平价格: %.3f万"%self.price_per_square
        print "\t保本涨幅比例: %.3f%%"%(promote * 100)
        print "\t贷款: %.3f万"%daikuan
        gap = real_pay - CURRENT_CASH
        sell_total_price = gap + DEBT
        sell_price_per_sq = sell_total_price / APARTMENT_SQ 
        print "自己房屋卖出底线:"
        print "\t最低卖出总价:%.3f万"%sell_total_price
        print "\t最低卖出每平均价:%.3f万"%sell_price_per_sq
        print "\t解抵押贷款额度:%.3f万"%DEBT
        print "\t解抵押后净得:%.3f"%(sell_total_price - DEBT)
        print "\t总可支配资金:%.3f"%(sell_total_price - DEBT + CURRENT_CASH)

if __name__ == "__main__":
    
    desc = "中铁国际城78平原值高"
    tp = 660
    wp = 364 
    op = 325
    area = 78
    location = LOC_5_6_RING
    is_man5_uniq = False
    is_man2 = True
    is_first = True
    lixi = 0.0
    ap = apartment(desc, tp, wp, op, area, location, is_man5_uniq, is_man2, is_first, lixi)
    ap.calc_RealPay()

    desc = "润泽悦溪89平南北通透满五唯一"
    tp = 725
    wp = PRICE_5_6_LIMIT 
    op = 80
    area = 89
    location = LOC_5_6_RING
    is_man5_uniq = True
    is_man2 = True
    is_first = True
    lixi = 0.0
    ap = apartment(desc, tp, wp, op, area, location, is_man5_uniq, is_man2, is_first, lixi)
    ap.calc_RealPay()
    
    """
    desc = "中铁国际城80平精装修方案二"
    wp = 500
    ap = apartment(desc, tp, wp, op, area, location, is_man5_uniq, is_man2, is_first, lixi)
    ap.calc_RealPay()
    desc = "润泽悦溪89平满五唯一"
    tp = 650
    wp = PRICE_5_6_LIMIT
    op = 87
    area = 87.0
    location = LOC_5_6_RING
    is_man5_uniq = True
    is_man2 = True
    is_first = True
    lixi = 0.0
    ap = apartment(desc, tp, wp, op, area, location, is_man5_uniq, is_man2, is_first, lixi)
    ap.calc_RealPay()
    """
