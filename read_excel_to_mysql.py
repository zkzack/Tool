#!/usr/bin/python
# coding:utf8

"""
@Version   :  v1.0
@Author    :  zack
@Software  :  PyCharm
@File      :  read_excel.py
@Time      :  2020/1/14 14:00
"""
import os

import pymysql
import warnings
import xlrd

'''  Readme
递归遍历文件夹下所有excel文件的数据并保存到mysql数据库

修改处：
1.修改 32行处的文件夹路径 
2.修改 72行处要保存数据的表名  
'''


class Read_Excel():
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect("192.168.5.192", "root", "123", charset="utf8")
        self.cursor = self.db.cursor()
        # 所有文件所在的文件夹目录
        self.path = r"C:\Users\Desktop\offic\meta_data"

        # self.path = path

    # 读取excel文件
    def read_excel(self):
        # 获取文件夹下所有文件的目录
        for root, dirs, files in os.walk(self.path):
            for file in files:
                # print(file)     #文件名
                # print(os.path.join(root, file))  #文件绝对路径

                # xlrd 读取excel文件中的数据
                data = xlrd.open_workbook(os.path.join(root, file))
                table = data.sheets()[0]

                # 遍历excel表中每一行的数据
                for nrow in range(1, table.nrows):
                    code = table.cell_value(nrow, 0)
                    pany_name = table.cell_value(nrow, 1)
                    state = table.cell_value(nrow, 2)
                    province = table.cell_value(nrow, 3)
                    city = table.cell_value(nrow, 4)
                    address = table.cell_value(nrow, 5)
                    deputy = table.cell_value(nrow, 6)
                    funds = table.cell_value(nrow, 7)
                    phone = table.cell_value(nrow, 8)
                    phone_2 = table.cell_value(nrow, 9)
                    email = table.cell_value(nrow, 10)
                    create_time = table.cell_value(nrow, 11)

                    r_list = [code, pany_name, state, province, city, address, deputy, funds, phone, phone_2, email, create_time]
                    # print(r_list)
                    self.writePage(r_list)

    # 将解析的数据保存到数据库
    def writePage(self, r_list):
        # f_db = 'create database if not exists zack_test charset utf8'
        f_use = 'use test'
        # f_tab = 'create table if not exists t_course(id VARCHAR(100),cName varchar(100),Intensity varchar(100),instrument varchar(100),part varchar(100));'
        f_ins = 'insert into qcc_data_zack_copy1(code,pany_name,state,province,city,address,deputy,funds,phone,phone_2,email,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        warnings.filterwarnings("ignore")
        try:
            # self.cursor.execute(f_db)
            self.cursor.execute(f_use)
            # self.cursor.execute(f_tab)
            self.cursor.execute(f_ins, r_list)
            self.db.commit()
        except Warning:
            pass

    # 主函数
    def run(self):
        self.read_excel()
        print("已保存到数据库")


if __name__ == "__main__":
    travel = Read_Excel()
    travel.run()
