# coding:utf-8
import pymysql
import time

# mysql数据库属性
host = '192.168.230.138'
port = 3306
username = 'root'
password = '123456'
database = 'yfs'


def getDb():
    # db = pymysql.connect(host, username, password, database, port)
    db = pymysql.connect(
        host=host,
        user=username,
        passwd=password,
        # db=database,
        port=port,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
    return db


def selectAll(sql):
    db = getDb()
    cursor = db.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    print(list)
    for row in list:
        print(row["name"])
        # id = row[0]
        # name = row[1]
        # age = row[2]
        # birth_date = row[3]
        # create_time = row[4]
        # print(create_time)
    db.close()


def insert():
    db = getDb()
    cursor = db.cursor()
    birth_date = '1991-04-22'  # time.strptime("1991-04-22", "%Y-%m-%d")
    current_time = '2019-09-28 12:00:05'  # time.strptime("%Y-%m-%d %H:%M:%S")
    sql = """INSERT INTO yfs.graze_user (name, age, birth_day, gmt_create) 
        VALUES ( '%s','%s','%s','%s');""" % ('yangfengshuai', 28, birth_date, current_time)
    try:
        insertResult = cursor.execute(sql)
        print(insertResult)
        db.commit()
    except UnicodeEncodeError as e:
        print(e)
        db.rollback()
    selectAll('select * from graze_user');
    new_id=cursor.lastrowid
    print(new_id)
    db.close()


def update(sql):
    db = getDb()
    cursor = db.cursor()
    try:
        updateCount = cursor.execute(sql)
        print(updateCount)
        db.commit()
        selectAll("select * from graze_user")
    except UnicodeEncodeError as e:
        print(e)
        db.rollback()
    db.close()


def delete(sql):
    db = getDb()
    cursor = db.cursor()
    try:
        delCount = cursor.execute(sql)
        print(delCount)
        db.commit()
        selectAll("select * from graze_user")
    except UnicodeEncodeError as e:
        print(e)
        db.rollback()

def selectAll1(sql):
    db = getDb()
    cursor = db.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    print(list)
    str = ""
    # for dict in list:
        # str = str + dict["COLUMN_NAME"] + ","
        # print(dict["COLUMN_NAME"])
    # str = str[:-1]
    print(str)
        # print(dict["column_comment"])
        # id = row[0]
        # name = row[1]
        # age = row[2]
        # birth_date = row[3]
        # create_time = row[4]
        # print(create_time)
    db.close()


# insert()
# update("update graze_user set age = 25")
# selectAll('select * from graze_user')
# selectAll1("select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name='graze_user' and table_schema='yfs'")
selectAll1("show databases")


# delete("delete from graze_user where id = 4 ")

