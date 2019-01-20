# -*- coding:utf-8 -*-

import pymysql

"""
    测试插入数据
@Author monkey
@Date 2019-1-20
"""


MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'whitesnake'  # 数据库名
MYSQL_USER = 'root'          # 数据库用户
MYSQL_PASSWORD = '123456'    # 数据库密码


table = 'short_comments'

conn = pymysql.connect(
    host=MYSQL_HOST,
    db=MYSQL_DBNAME,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
    use_unicode=False)

with conn:
    cursor = conn.cursor()

__table = 'short_comments_test'

def create_database():
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
        "`content` TEXT,"
        "PRIMARY KEY(id)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8".format(__table)
    )

    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print('===== 成功创建数据库表 =====')
    except Exception as e:
        print('===== 创建数据库表出现异常 =====\n %s', e)


def insert_comments(datalsit):
    """ 往数据库表中插入数据 """
    insert_sql = (
        "insert into "
        "{} "
        "values("
        "%s"
        ")".format(__table))

    try:
        for comment in datalsit:
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
            # cursor.execute(insert_sql, data)
        cursor.executemany(insert_sql, datalsit)
        conn.commit()
        print("===== 成功插入", len(datalsit), "数据  =====")
    except Exception as e:
        print('===== insert exception -->>> %s', e)

"""
        "nickName, "
        "userId, "
        "userLevel, "
        "cityName, "
        "gender, "
        "score, "
        "startTime, "
        "filmView, "
        "supportComment, "
        "supportLike, "
        "sureViewed, "
        "avatarurl, "
        "content"


==============
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s, "
        "%s"


"""

data = {
	'id': 1052089562,
	'nickName': '🐾洋洋得意💋',
	'userId': 1780375374,
	'userLevel': 3,
	'cityName': '西宁',
	'gender': None,
	'score': 5,
	'startTime': '2019-01-20 20:38:51',
	'filmView': False,
	'supportComment': True,
	'supportLike': True,
	'sureViewed': 1,
	'avatarurl': 'https://img.meituan.net/maoyanuser/350bff22b2ac2c7e5b11937b8dc8f9d212207.png',
	'content': '可以，不错，值得一看'
}

datalist = []
datalist.append(data)

# create_database()
insert_comments(datalist)
