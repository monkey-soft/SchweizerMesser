# -*- coding:utf-8 -*-

import json
import os
import threading
import urllib
from queue import Queue
import random
import requests
import time

"""
    使用多线程将 Unsplash 的图片下载到本地
@Author monkey
@Date 2018-6-19
"""
# 使用队列保存存放图片 url 地址, 确保线程同步
url_queue = Queue()
# 线程总数
THREAD_SUM = 5
# 存储图片的位置
IMAGE_SRC = 'D://Unsplash/'


class Unsplash(threading.Thread):

    NOT_EXIST = 0

    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        while not self.NOT_EXIST:
            # 队列为空, 结束线程
            if url_queue.empty():
                NOT_EXIST = 1
                break

            url = url_queue.get()
            self.get_data(url)
            time.sleep(random.randint(3, 5))

    def get_data(self, url):
        """ 根据 url 获取 JSON 格式的图片数据"""
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'referer': 'https://unsplash.com/',
            'path': url.split('com')[1],
            'authority': 'unsplash.com',
            'viewport-width': '1920',
        }
        response = requests.get(url, headers=headers)
        print('请求第[ ' + url + ' ], 状态码为 ', response.status_code)
        self.get_image_url(response.text)

    def get_image_url(self, response):
        """
        使用 json.loads(response) 将其转化为字典类型, 以便采用 key-value 形式获取值
        raw：包含Exif信息的全尺寸原图，此类图片的容量很大
        full：全尺寸分辨率的图片，去除了Exif信息并且对内容进行了压缩，图片容量适中
        normal：普通尺寸的图片，去除了Exif信息，并且对分辨率和内容进行了压缩，图片容量较小；
        """
        image_url = json.loads(response)[0]['urls']['full']
        self.save_img(image_url)

    def save_img(self, image_url):
        print('线程', self.thread_id, ' | 正在下载', image_url)
        try:
            if not os.path.exists(IMAGE_SRC):
                os.mkdir(IMAGE_SRC)
            filename = IMAGE_SRC + image_url.split('com')[1].split('?')[0] + '.jpg'
            # 下载图片，并保存到文件夹中
            urllib.request.urlretrieve(image_url, filename=filename)
        except IOError as e:
            print('保存图片出现异常失败', e)


def get_all_url():
    """ 循环计算出所有的 url 地址, 存放到队列中 """
    base_url = 'https://unsplash.com/napi/photos?page={}&per_page=1&order_by=latest'
    page = 1
    max_page = 71131
    while page <= max_page:
        url = base_url.format(page)
        url_queue.put(url)
        page += 1
    print('计划下载', url_queue.qsize(), '张图片')


if __name__ == '__main__':
    get_all_url()
    for i in range(THREAD_SUM):
        unsplash = Unsplash(i+1)
        unsplash.start()
