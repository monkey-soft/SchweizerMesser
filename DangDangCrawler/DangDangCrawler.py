# -*- coding:utf-8 -*-
import urllib.request
import time
import csv
import codecs
from bs4 import BeautifulSoup

'''
项目说明：
【1】抓取以 Python 为关键字搜索出来的书籍，并保存到 csv 文件中。
【2】该项目是 **urllib**、**re**、**BeautifulSoup** 这三个库的用法的实战篇。
'''
def main():
    # 爬取地址, 当当所有 Python 的书籍, 一共是 21 页
    url = "http://search.dangdang.com/?key=python&act=input&show=big&page_index="
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    # 代理, 如果在需要代理就加上这行代码
    # proxy_handler = urllib.request.ProxyHandler({
    #
    # })
    # opener = urllib.request.build_opener(proxy_handler)
    # urllib.request.install_opener(opener)

    index = 1
    while index <= 21:
        # 发起请求
        request = urllib.request.Request(url=url+str(index), headers=headers)
        response = urllib.request.urlopen(request)
        index = index + 1
        # 解析爬取内容
        parse_content(response)
        time.sleep(1)  # 休眠1秒

    show_result()


def parse_content(response):
    # 提取爬取内容中的 a 标签, 例如：
    # <a
    #     class="pic" dd_name="单品图片"
    #     ddclick="act=normalResult_picture&amp;pos=23648843_53_2_q"
    #     href="http://product.dangdang.com/23648843.html"
    #     name="itemlist-picture"
    #     target="_blank" title="
    #     趣学Python――教孩子学编程 ">
    #
    #   <img
    #       alt=" 趣学Python――教孩子学编程 "
    #       data-original="http://img3x3.ddimg.cn/20/34/23648843-1_b_0.jpg"
    #       src="images/model/guan/url_none.png"/>
    # </a>
    soup = BeautifulSoup(response)
    temps = soup.find_all('a', class_='pic')
    global books
    books = books + temps
    print('get books size = ' + str(len(books)))


def show_result():
    file_name = 'PythonBook.csv'

    # 指定编码为 utf-8, 避免写 csv 文件出现中文乱码
    with codecs.open(file_name, 'w', 'utf-8') as csvfile:
        filednames = ['书名', '页面地址', '图片地址']
        writer = csv.DictWriter(csvfile, fieldnames=filednames)

        writer.writeheader()
        for book in books:
            print(book)
            # print(book.attrs)
            # 获取子节点<img>
            # (book.children)[0]
            if len(list(book.children)[0].attrs) == 3:
                img = list(book.children)[0].attrs['data-original']
            else:
                img = list(book.children)[0].attrs['src']

            try:
                writer.writerow({'书名':book.attrs['title'], '页面地址':book.attrs['href'], '图片地址': img})
            except UnicodeEncodeError:
                print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

    print('将数据写到 ' + file_name + '成功！')


if __name__ == '__main__':
    books = []
    main()
