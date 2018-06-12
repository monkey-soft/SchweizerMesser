
### Python小工具集合

#### 1) [字符串去重](./CutDownRepetition)
> 说明

将文件（如：txt）中重复的字符串过滤掉。

#### 2) [端口扫描器](./PortScanner)
> 说明:
* 使用全握手协议的TCP来判断端口的可用性
* 对一或者多个端口进行扫描
* 使用多线程进行扫描, 加速扫描速度　
* -p参数后面不加端口号, 即扫描目标主机的常见端口
* -a参数： 扫描1-65535个端口
* 发送TCP SYN包来判断端口是否开放（暂不支持）
        
> 参数用法：
   
* -H 指定目标主机。
  * 示例1: -H www.baidu.com 
  * 示例2: -H 192.168.1.1
* -p 指定目标端口, 不填写就默认是扫描常见端口(常见端口见代码)
* -a 是否扫描所有端口（1 - 65535）, 默认是Flase, 即不扫描
   * 示例：-a True
            
#### 3) [当当爬虫](./DangDangCrawler)
> 说明

- 详细用法可以阅读 [爬虫实战一：爬取当当网所有 Python 书籍](https://mp.weixin.qq.com/s/_IKBJEkh9HtNhpJEbwsD6Q)
- 抓取以 Python 为关键字搜索出来的书籍，并保存到 csv 文件中。
- 该项目是 **urllib**、**re**、**BeautifulSoup** 这三个库的用法的实战篇

#### 4) [网易云音乐精彩评论爬虫](./NeteaseMusic)
> 说明

- 详细用法可以阅读 [爬取网易云音乐精彩评论](https://mp.weixin.qq.com/s/tMVu8dUepSPIvm3yCMUt1g)
- 爬取动态渲染页面(使用 ajax 加载数据)
- 爬取网易云音乐部分歌曲的精彩评论

#### 5) [爬取网易云音乐单首歌曲的所有评论](./NeteaseMusic2)
> 说明

- 详细用法可以阅读 [爬取《Five Hundred Miles》在网易云音乐的所有评论](https://mp.weixin.qq.com/s/kcA-6WEHWQ-DOwxtWtYjWw)
- 使用 Selenium 爬取动态渲染页面(使用 ajax 加载数据)
- 存储数据到 MongoDB 
- 使用 Selenium 爬取《Five Hundred Miles》 在网易云音乐的所有评论, 然后存储到 MongoDB 中。

### 写在最后
该仓库会持续更新...

如果在您使用过程中遇到问题，可以到我的微信公众号『极客猴』留言。