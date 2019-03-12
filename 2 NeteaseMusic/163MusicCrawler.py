# -*- coding:utf-8 -*-

import json
import random

import requests
import time
import csv
import codecs


"""
    爬取网易云音乐歌曲的精彩评论
@Author monkey
@Date 2018-6-6
"""


def start_spider(song_id):
    """ 评论数据采用 AJAX 技术获得, 下面才是获取评论的请求地址 """
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/song?id={}'.format(song_id),
    }

    formdata = {
        'params': '57Wh2mgebLOOPQVBc+B2wz4sCCH/nXZFEoTc/XNySiqT0V7ZxUADzDNgTXXhYgAJ5BNMryMgxhdwNzF1GyxDZo3iR9/YYbWgCAQHC5DCDuObqvxNcOcnQDaRqJCrqQcrEABW1SwKitfbD3wMEyB4tJu+rU8goSwg2FP/PBBLs9DVs1iWdWGjV6CdrocA36Rs',
        'encSecKey': '63774137ba4f5cc60d1b6a3bc14985a9563a7bfdec4f3e74297ffc07514adf18f90620933a01c2db4ca989cc4e1dfc49789981424c294a34e48c2cbe7aa51533a5cc5b5776a9e499cd08770bc596655dbe8e001d1ed5fd47a27dd195128480820cc67a799d341f95d447e3522851f2b64ad1cb8350e2015b265b9e684179351c',
    }

    response = requests.post(url, headers=headers, data=formdata)
    print('请求 [ ' + url + ' ], 状态码为 ')
    print(response.status_code)
    # get_hot_comments(response.text)
    # 将数据写到 CSV 文件中
    write_to_file(get_hot_comments(response.text))


def get_hot_comments(response):
    """ 获取精彩评论
    请求返回结果是 Json 数据格式, 使用 json.loads(response) 将其转化为字典类型, 就可以使用 key-value 形式获取值
    """
    data_list = []
    data = {}

    for comment in json.loads(response)['hotComments']:
        data['userId'] = comment['user']['userId']
        data['nickname'] = comment['user']['nickname']
        data['content'] = comment['content']
        data['likedCount'] = comment['likedCount']
        data_list.append(data)
        data = {}
    # print(data_list)
    return data_list


def write_to_file(datalist):
    print('开始将数据持久化……')
    file_name = '网易云音乐精彩评论.csv'

    with codecs.open(file_name, 'a+', 'GBK') as csvfile:
        filednames = ['用户Id', '昵称', '评论内容', '点赞数']
        writer = csv.DictWriter(csvfile, fieldnames=filednames)

        writer.writeheader()
        for data in datalist:
            print(data)
            try:
                writer.writerow({filednames[0]: data['userId'],
                                 filednames[1]: data['nickname'],
                                 filednames[2]: data['content'],
                                 filednames[3]: data['likedCount']})
            except UnicodeEncodeError:
                print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

    print('成功将数据写入到 ' + file_name + ' 中！')


def get_song_id(url):
    """ 从 url 中截取歌曲的 id """
    song_id = url.split('=')[1]
    return song_id


def main():
    songs_url_list = [
        'http://music.163.com/#/song?id=186016',  # 晴天
        'http://music.163.com/#/song?id=186001',  # 七里香
        'http://music.163.com/#/song?id=27876900',  # Here We Are Again 《喜剧之王》电影插曲
        'http://music.163.com/#/song?id=439915614',  # 刚好遇见你
        'http://music.163.com/#/song?id=139774',  # The truth that you leave
        'http://music.163.com/#/song?id=29567189',  # 理想
        'http://music.163.com/#/song?id=308353',  # 钟无艳
        'http://music.163.com/#/song?id=31445772',  # 理想三旬
        'http://music.163.com/#/song?id=439915614',  # 刚好遇见你
        'http://music.163.com/#/song?id=28815250',  # 平凡之路
        'http://music.163.com/#/song?id=25706282',  # 夜空中最亮的星
        'http://music.163.com/#/song?id=436514312',  # 成都
    ]

    for each in songs_url_list:
        start_spider(get_song_id(each))
        time.sleep(random.randint(5, 8))


if __name__ == '__main__':
    main()

