'''
author:zack
'''
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from spider.spider_film import Film_Recommend
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost:3306/f4"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db = SQLAlchemy(app)

# 电影推荐实体类
class Film(db.Model):
    __tablename__ = 'film'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))        #电影名称
    score = db.Column(db.Float)             #电影评分
    release_date =db.Column(db.String(40))  #上映时间
    types = db.Column(db.String(40))        #电影类型
    regions = db.Column(db.String(40))      #制片地区
    url = db.Column(db.String(100))         #豆瓣链接

    def __init__(self, name, score, release_date, types, regions, url):
        self.tname = name
        self.tage = score
        self.release_date = release_date
        self.types = types
        self.tbirth = regions
        self.url = url

db.create_all()

# 电影首页视图处理
@app.route('/index',methods=['POST','GET'])
def index():
    if request.method == 'Get':
        return render_template('film.html')
    else:
        type = request.form.get('type','科幻')
        number = request.form.get('number','7')
        zz = Film_Recommend(type, number)
        zz.run()
    film = Film.query.order_by(db.desc(Film.id)).filter(Film.types.like("%{}%".format(type))).limit(number).all()
    return render_template('movie.html', film=film)


# 电影视图处理
@app.route('/film',methods=['POST','GET'])
def film_rec():
    if request.method == 'GET':
        return render_template('film.html')
    else:
        # 接收用户输入的电影类型
        type = request.form.get('type')
        # 定义主流电影类型 
        kinds = ["剧情", "喜剧", "动作", "爱情", "科幻",
                 "悬疑", "惊悚", "恐怖", "战争", "犯罪",
                 "奇幻", "冒险"," 灾难", "武侠", "古装"]
        # 输入类型错误提示
        if type not in kinds:
            msg1 = "Sorry! 该类型暂未收录,请重新输入!"
            msg2 = "如: 喜剧"
            return render_template('film.html',msg1=msg1,msg2=msg2)
        else:
            # 获取用户输入的推荐数量
            number = request.form.get('number')
            # 调用爬虫，获取电影信息，并保存到数据库
            zz = Film_Recommend(type,number)
            zz.run()
        # 从数据库获取电影信息，呈现给用户
        film = Film.query.order_by(db.desc(Film.id)).filter(Film.types.like("%{}%".format(type))).limit(number).all()
        return render_template('movie.html', film=film)


# 查询数据库中已获取的所有电影
@app.route('/movie')
def movie():
    film = Film.query.order_by(db.asc(Film.id)).all()
    return render_template('movie.html', film=film)



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')