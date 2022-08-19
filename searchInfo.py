# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 0019 19:23
# @Author  : Leo.W
# @Email   : wanglei@whu.edu.cn
# @File    : google_api.py


from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
import sys
sys.path.append("..")


# 配置数据库的地址--'mysql://账户名:密码@ip地址:端口/数据库名'********自定义
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:xxxx@xx.xx.xx.xx:xx/google_db'

# 跟踪数据库的修改 --> 不建议开启 未来的版本中会移除
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#查询时会显示原始SQL语句
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


def db_import(f_keyword, db_name, title, caption_cite, caption_time, caption_p):

    # 数据库的模型, 需要继承db.Model
    class Dict(db.Model):
        # 定义表名
        __tablename__ = f'{f_keyword}_{db_name}'
        # 定义字段
        # db.Column表示是一个字段
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        caption_time = db.Column(db.Text)
        title = db.Column(db.Text)
        caption_cite = db.Column(db.Text)
        caption_p = db.Column(db.Text)

        # repr()方法显示一个可读字符串,实例返回的内容
        def __repr__(self):
            return '<Role: %s %s %s %s>' % (self.title, self.caption_cite, self.caption_time, self.caption_p)

    # 删除表
    # db.drop_all()
    # 创建表
    db.create_all()
    for i in range(len(title)):
        d = Dict(caption_time=caption_time[i], title=title[i], caption_cite=caption_cite[i], caption_p=caption_p[i])
        db.session.add(d)
        db.session.commit()





