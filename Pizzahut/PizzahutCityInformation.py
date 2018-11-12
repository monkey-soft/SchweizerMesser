# -*- coding:utf-8 -*-

from urllib.parse import quote
from lxml import etree

import json
import requests
import time

"""
    爬取全国各大城市的必胜客餐厅
@Author monkey
@Date 2018-11-8
"""

# 全国有必胜客餐厅的城市, 我将城市放到文件中, 一共 380 个城市
cities = []


def get_cities():
    """ 从文件中获取城市 """
    file_name = 'cities.txt'
    with open(file_name, 'r', encoding='UTF-8-sig') as file:
        for line in file:
            city = line.replace('\n', '')
            cities.append(city)

    results = {}
    # 依次遍历所有城市的餐厅
    for city in cities:
        restaurants = get_stores(city)
        results[city] = restaurants
        time.sleep(2)

    with open('results.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(results, indent=4, ensure_ascii=False))


def get_stores(city):
    """ 根据城市获取餐厅信息 """
    session = requests.Session()
    # 对【城市|0|0】进行 Url 编码
    city_urlencode = quote(city + '|0|0')
    # 获取首页的 cookies
    cookies = requests.cookies.RequestsCookieJar()

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Host': 'www.pizzahut.com.cn',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

    print('============', city, '============')
    resp_from_index = session.get('http://www.pizzahut.com.cn/', headers=headers)
    # print(resp_from_index.cookies)
    # 然后将原来 cookies 的 iplocation 字段，设置自己想要抓取城市。
    cookies.set('AlteonP', resp_from_index.cookies['AlteonP'], domain='www.pizzahut.com.cn')
    cookies.set('iplocation', city_urlencode, domain='www.pizzahut.com.cn')
    # print(cookies)

    page = 1
    restaurants = []

    while True:
        data = {
            'pageIndex': page,
            'pageSize': "50",
        }

        response = session.post('http://www.pizzahut.com.cn/StoreList/Index', headers=headers, data=data, cookies=cookies)
        html = etree.HTML(response.text)
        # 获取餐厅列表所在的 div 标签
        divs = html.xpath("//div[@class='re_RNew']")
        temp_items = []
        for div in divs:
            item = {}
            content = div.xpath('./@onclick')[0]
            # ClickStore('22.538912,114.09803|城市广场|深南中路中信城市广场二楼|0755-25942012','GZH519')
            # 过滤掉括号和后面的内容
            content = content.split('(\'')[1].split(')')[0].split('\',\'')[0]

            if len(content.split('|')) == 4:
                item['coordinate'] = content.split('|')[0]
                item['restaurant_name'] = content.split('|')[1] + '餐厅'
                item['address'] = content.split('|')[2]
                item['phone'] = content.split('|')[3]
            else:
                item['restaurant_name'] = content.split('|')[0] + '餐厅'
                item['address'] = content.split('|')[1]
                item['phone'] = content.split('|')[2]
            print(item)
            temp_items.append(item)

        if not temp_items:
            break
        restaurants += temp_items
        page += 1
        time.sleep(2)
    return restaurants


if __name__ == '__main__':
    get_cities()
