import requests
import pymysql
import json
import warnings

class Film_Recommend():
    def __init__(self,type=None,number=None):
        self.type = type
        self.number = number
        self.headers = {"User-Agent": "Mozilla/5.0"}
        # 要获取信息的网页链接
        self.url = "https://movie.douban.com/j/chart/top_list?"
        # 连接数据库
        self.db = pymysql.connect("localhost", "root", "123456", charset="utf8")
        self.cursor = self.db.cursor()

    # 获取页面信息
    def getPage(self, params):
        res = requests.get(self.url, params=params, headers=self.headers)
        res.encoding = "utf-8"
        html = res.text
        # 将获取的信息进行解析
        self.parsePage(html)

    # 解析页面信息，提取所需信息
    def parsePage(self, html):
        # html为json格式的字符串
        info = json.loads(html)
        # for循环遍历html中的元素
        for film in info:
            # 电影名称
            name = film["title"]
            # 电影评分
            score = float(film["score"].strip())
            # 电影上映日期
            release_date = film["release_date"]
            # 电影类型
            types = '/'.join(film["types"])
            # 电影制片国家/地区
            regions = '/'.join(film["regions"])
            # 电影详情连接
            url = film['url']
            film_list = [name, score, release_date, types, regions ,url]
            # 将提取的信息保存到数据库
            self.savePage(film_list)

    # 将解析的数据保存到数据库
    def savePage(self, film_list):
        # 创建数据库
        f_db = 'create database if not exists f4 charset utf8'
        f_use = 'use f4'
        f_tab = 'create table if not exists film(id int primary key auto_increment,\
                        name varchar(100),score float,release_date varchar(40),\
                        types varchar(40),regions varchar(40),url varchar(100));'
        f_ins = 'insert into film(name,score,release_date,types,regions,url) values(%s,%s,%s,%s,%s,%s)'

        # 将信息保存到数据库中
        warnings.filterwarnings("ignore")
        try:
            self.cursor.execute(f_db)
            self.cursor.execute(f_use)
            self.cursor.execute(f_tab)
            self.cursor.execute(f_ins, film_list)
            self.db.commit()
        except Warning:
            pass

    # 主函数
    def run(self):
        dic = {
            "剧情": "11",
            "喜剧": "24",
            "动作": "5",
            "爱情": "13",
            "科幻": "17",
            "悬疑": "10",
            "惊悚": "19",
            "恐怖": "20",
            "战争": "22",
            "犯罪": "3",
            "奇幻": "16",
            "冒险": "15",
            "灾难": "12",
            "武侠": "19",
            "古装": "30"
        }
        filmType = dic[self.type]
        params = {
            "type": filmType,
            "interval_id": "100:90",
            "action": "",
            "start": "0",
            "limit": self.number
        }
        # 根据用户选择的信息获取页面信息
        self.getPage(params)
        # 断开数据库连接
        self.cursor.close()
        self.db.close()

























