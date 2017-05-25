#-*- coding:utf-8 -*-

from Crawler import Shopee

import datetime

t1 = datetime.datetime.now()

keyword = '手工皂'
products = Shopee.search_product(keyword)
if products != None:
    for product_list in [products[i:i+10] for i in range(0, len(products), 10)]:
        detail_list, failed_list = Shopee.load_product_details(map(lambda r: r['path'].encode('utf-8'), product_list))
        print detail_list

t2 = datetime.datetime.now()

print t2 - t1
