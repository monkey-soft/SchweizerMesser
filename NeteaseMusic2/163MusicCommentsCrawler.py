# -*- coding:utf-8 -*-

import pymongo
import random
import time
from math import ceil
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
    使用 Selenium 爬取网易云音乐歌曲的所有评论
    数据存储到 Mongo 数据库中
@Author monkey
@Date 2018-6-10
"""

MONGO_HOST = '127.0.0.1'
MONGO_DB = '163Music'
MONGO_COLLECTION = 'comments'

client = pymongo.MongoClient(MONGO_HOST)
db_manager = client[MONGO_DB]


def start_spider(url):
    """  """
    # 会启动 Chrome 浏览器访问页面
    """
    # 从 Chrome 59 版本, 支持 Headless 模式(无界面模式), 即不会弹出浏览器
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    brower = webdriver.Chrome(chrome_options=chrome_options)
    """
    brower = webdriver.Chrome()
    brower.get(url)
    # 等待 5 秒, 让评论数据加载完成
    time.sleep(5)
    # 页面嵌套一层 iframe, 必须切换到 iframe, 才能定位的到 iframe 里面的元素
    iframe = brower.find_element_by_class_name('g-iframe')
    brower.switch_to.frame(iframe)
    # 获取【最新评论】总数
    new_comments = brower.find_elements(By.XPATH, "//h3[@class='u-hd4']")[1]

    max_page = get_max_page(new_comments.text)
    current = 1
    is_first = True
    while current <= max_page:
        print('正在爬取第', current, '页的数据')
        if current == 1:
            is_first = True
        else:
            is_first = False
        data_list = get_comments(is_first, brower)
        save_data_to_mongo(data_list)
        time.sleep(1)
        go_nextpage(brower)
        # 模拟人为浏览
        time.sleep(random.randint(8, 12))
        current += 1


def get_comments(is_first, brower):
    """ 获取评论数据 """
    items = brower.find_elements(By.XPATH, "//div[@class='cmmts j-flag']/div[@class='itm']")
    # 首页的数据中包含 15 条精彩评论, 20 条最新评论, 只保留最新评论
    if is_first:
        items = items[15: len(items)]

    data_list = []
    data = {}
    for each in items:
        # 用户 id
        userId = each.find_elements_by_xpath("./div[@class='head']/a")[0]
        userId = userId.get_attribute('href').split('=')[1]
        # 用户昵称
        nickname = each.find_elements_by_xpath("./div[@class='cntwrap']/div[1]/div[1]/a")[0]
        nickname = nickname.text
        # 评论内容
        content = each.find_elements_by_xpath("./div[@class='cntwrap']/div[1]/div[1]")[0]
        content = content.text.split('：')[1]  # 中文冒号
        # 点赞数
        like = each.find_elements_by_xpath("./div[@class='cntwrap']/div[@class='rp']/a[1]")[0]
        like = like.text
        if like:
            like = like.strip().split('(')[1].split(')')[0]
        else:
            like = '0'
        # 头像地址
        avatar = each.find_elements_by_xpath("./div[@class='head']/a/img")[0]
        avatar = avatar.get_attribute('src')

        data['userId'] = userId
        data['nickname'] = nickname
        data['content'] = content
        data['like'] = like
        data['avatar'] = avatar
        print(data)
        data_list.append(data)
        data = {}
    return data_list


def save_data_to_mongo(data_list):
    """ 一次性插入 20 条评论。
        插入效率高, 降低数据丢失风险
    """
    collection = db_manager[MONGO_COLLECTION]
    try:
        if collection.insert_many(data_list):
            print('成功插入', len(data_list), '条数据')
    except Exception:
        print('插入数据出现异常')


def go_nextpage(brower):
    """ 模拟人为操作, 点击【下一页】 """
    next_button = brower.find_elements(By.XPATH, "//div[@class='m-cmmt']/div[3]/div[1]/a")[-1]
    if next_button.text == '下一页':
        next_button.click()


def get_max_page(new_comments):
    """ 根据评论总数, 计算出总分页数 """
    print('=== ' + new_comments + ' ===')
    max_page = new_comments.split('(')[1].split(')')[0]
    # 每页显示 20 条最新评论
    offset = 20
    max_page = ceil(int(max_page) / offset)
    print('一共有', max_page, '个分页')
    return max_page


if __name__ == '__main__':
    url = 'http://music.163.com/#/song?id=27759600'  # Five Hundred Miles
    start_spider(url)
