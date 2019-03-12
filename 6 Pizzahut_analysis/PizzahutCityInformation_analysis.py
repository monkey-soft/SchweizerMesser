# -*- coding:utf-8 -*-

from pyecharts import Bar
from pyecharts import Pie
from pyecharts import configure

import json


"""
    可视化分析全国各大城市的必胜客餐厅
@Author monkey
@Date 2018-11-25
"""


def get_datas():
    """ 从文件中获取数据 """
    file_name = 'results.json'
    with open(file_name, 'r', encoding='UTF-8') as file:
        content = file.read()
        data = json.loads(content, encoding='UTF-8')
        # print(data)
    return data


def count_restaurants_sum(data):
    """ 对字典进行遍历, 统计每个城市的餐厅总数 """
    results = {}
    for key, value in data.items():
        results[key] = len(value)
        # print(key, len(value))
    return results


def clean_datas(data):
    """
    清除脏数据。
    经过分析发现 ('新区', 189), ('南区', 189), ('朝阳', 56) 是脏数据, 必胜客官网的地区选项中就有这三个名字
    [('新区', 189), ('上海市', 189), ('南区', 189), ('北京市', 184), ('深圳', 95),
     ('广州', 86), ('杭州', 78), ('天津市', 69), ('朝阳', 56), ('苏州', 54)]
    """
    data.remove(('新区', 189))
    data.remove(('南区', 189))
    data.remove(('朝阳', 56))
    return data


def render_top10():
    """
    绘制直方图显示 全国必胜客餐厅总数 Top 10 的城市
    根据清洗过后数据的结果, Top 城市如下
    ('上海市', 189), ('北京市', 184), ('深圳', 95), ('广州', 86), ('杭州', 78),
    ('天津市', 69), ('苏州', 54), ('西安', 52), ('武汉', 51), ('成都', 48)
    """
    attr = ["上海", "北京", "深圳", "广州", "杭州", "天津", "苏州", "西安", "武汉", "成都"]
    values = [189, 184, 95, 86, 78, 69, 54, 52, 51, 48]
    bar = Bar("全国各大城市必胜客餐厅数量排行榜")
    bar.add("总数", attr, values, is_stack=True, is_more_utils=True)
    bar.render("render_bar.html")


def count_other_sum(data):
    count = 0
    for each in data:
        count += each[1]
    print("全国餐厅总数：", count)
    print("剔除北上广深：", count-189-184-95-86)


def render_top10_percent():
    """
    绘制饼状图 显示北上广深餐厅数在全国中的比例
    """
    configure(global_theme='macarons')
    attr = ["上海", "北京", "深圳", "广州", "其他城市"]
    value = [189, 184, 95, 86, 1893]  # 根据 count_other_sum() 计算出来的
    pie = Pie("北上广深餐厅数的占比")
    pie.add("", attr, value, is_label_show=True, is_more_utils=True)
    pie.render("render_pie.html")


def main():
    informs = get_datas()
    restaurants_sum = count_restaurants_sum(informs)
    # 将字典中的每个 key-value 转化为元组，然后根据 value 进行倒序排序
    restaurants_sum = sorted(restaurants_sum.items(), key=lambda item: item[1], reverse=True)
    # 清除脏数据
    restaurants_sum = clean_datas(restaurants_sum)
    print(restaurants_sum)
    render_top10()

    # 计算除北上广深之外餐厅总数
    count_other_sum(restaurants_sum)
    render_top10_percent()


if __name__ == '__main__':
    main()
