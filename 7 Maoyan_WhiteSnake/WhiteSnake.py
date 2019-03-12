# -*- coding:utf-8 -*-

import json
import pymysql
import random
import requests
import time


"""
    抓取猫眼 《白蛇：缘起》的短片
@Author monkey
@Date 2019-1-20
"""

# Mysql 配置信息
# Mysql 数据库建议使用 5.5 或者 5.5 以上的版本
# 根据你的环境修改
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'whitesnake'  # 数据库名
MYSQL_USER = 'root'          # 数据库用户
MYSQL_PASSWORD = '123456'    # 数据库密码


class WhiteSnakeSpider(object):

    def __init__(self):
        # 数据库表
        self.__table = 'short_comments'

        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            charset='utf8mb4',
            use_unicode=False)

        with self.conn:
            self.cursor = self.conn.cursor()

    def create_database(self):
        """ 截止到 2019.1.20,
            影片一共有 12.7 万人评分
            数据量比较大, 所以选择将数据存储到数据库中
        """
        create_table_sql = (
            # "DROP TABLE IF EXISTS {};"
            "CREATE TABLE IF NOT EXISTS {} ("
            "`id` VARCHAR(12) NOT NULL,"
            "`nickName` VARCHAR(30),"
            "`userId` VARCHAR(12),"
            "`userLevel` INT(3),"
            "`cityName` VARCHAR(10),"
            "`gender` tinyint(1),"
            "`score` FLOAT(2,1),"
            "`startTime` VARCHAR(30),"
            "`filmView` BOOLEAN,"
            "`supportComment` BOOLEAN,"
            "`supportLike` BOOLEAN,"
            "`sureViewed` INT(2),"
            "`avatarurl` VARCHAR(200),"
            "`content` TEXT"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4".format(self.__table)
        )

        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print('===== 成功创建数据库表 =====')
        except Exception as e:
            self.close_connection()
            print('===== 创建数据库表出现异常 =====\n %s', e)

    def insert_comments(self, datalist):
        """ 往数据库表中插入数据 """
        insert_sql = (
            "insert into "
            "{} (id, nickName, userId, userLevel, cityName, gender, score, "
            "startTime, filmView, supportComment, supportLike, sureViewed, avatarurl, content)"
            "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(self.__table))

        try:
            templist = []
            for comment in datalist:
                if comment.get('gender') is None:
                    comment['gender'] = -1
                data = (comment.get('id'),
                        comment.get('nickName'),
                        comment.get('userId'),
                        comment.get('userLevel'),
                        comment.get('cityName'),
                        comment.get('gender'),
                        comment.get('score'),
                        comment.get('startTime'),
                        comment.get('filmView'),
                        comment.get('supportComment'),
                        comment.get('supportLike'),
                        comment.get('sureViewed'),
                        comment.get('avatarurl'),
                        comment.get('content'))
                templist.append(data)
            self.cursor.executemany(insert_sql, templist)
            self.conn.commit()
        except Exception as e:
            print('===== insert exception -->>> %s', e)

    def close_connection(self):
        """ 关闭数据库连接 """
        # 关闭游标连接
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

    def get_shorts_comments(self):
        """ 构造会话 Session 抓取短片 """
        session = requests.Session()
        # 电影短片的 API 接口地址
        movie_url = 'http://m.maoyan.com/mmdb/comments/movie/1235560.json?_v_=yes&offset={}'

        headers = {
            'User-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Host': 'm.maoyan.com',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        offset = 1
        while 1:
            print('============抓取第', offset, '页短评============')
            print('============>>>', movie_url.format(offset))
            response = session.get(movie_url.format(offset), headers=headers)
            if response.status_code == 200:
                """ 解析短评
                请求返回结果是 Json 数据格式, 具体见 sample.json
                使用 json.loads(response) 将其转化为字典类型, 就可以使用 key-value 形式获取值
                """
                data_list = []
                data = {}
                for comment in json.loads(response.text)['cmts']:
                    data['id'] = comment.get('id')
                    data['nickName'] = comment.get('nickName')
                    data['userId'] = comment.get('userId')
                    data['userLevel'] = comment.get('userLevel')
                    data['cityName'] = comment.get('cityName')
                    data['gender'] = comment.get('gender')
                    data['score'] = comment.get('score')
                    data['startTime'] = comment.get('startTime')
                    data['filmView'] = comment.get('filmView')
                    data['supportComment'] = comment.get('supportComment')
                    data['supportLike'] = comment.get('supportLike')
                    data['sureViewed'] = comment.get('sureViewed')
                    data['avatarurl'] = comment.get('avatarurl')
                    data['content'] = comment.get('content')
                    print(data)
                    data_list.append(data)
                    data = {}
                print('============解析到', len(data_list), '条短评数据============')
                self.insert_comments(data_list)
            else:
                # 抓取失败就先暂停抓取, 标记抓取页数, 过段时间再抓取
                print('>=== 抓取第 ', offset, ' 失败, 错误码为 ' + response.status_code)
                break
            offset += 1
            time.sleep(random.randint(10, 20))
        self.close_connection()


if __name__ == '__main__':
    spider = WhiteSnakeSpider()
    spider.create_database()
    spider.get_shorts_comments()
