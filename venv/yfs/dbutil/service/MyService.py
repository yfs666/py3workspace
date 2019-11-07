import pymysql
import time

# mysql数据库属性
host = '192.168.230.138'
port = 3306
username = 'root'
password = '123456'
database = 'yfs'
def getDb():
    db = pymysql.connect(
        host=host,
        user=username,
        passwd=password,
        db=database,
        port=port,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
    return db


def selectExecute(sql):
    db = getDb()
    cursor = db.cursor()
    cursor.execute(sql)
    dataList = cursor.fetchall()
    columnNameList = []
    if dataList:
        for (k, v) in dataList[0].items():
            columnNameList.append(k)
    return columnNameList, dataList


def query_tables(table_name):
    db = getDb()
    cursor = db.cursor()
    cursor.execute("show tables")
    data_list = cursor.fetchall()
    tables = []
    if data_list:
        for table_detail in data_list:
            for (k, v) in table_detail.items():
                if table_name in v:
                 tables.append(v)
    return tables


def query_columns(table_name):
    sql = "select column_name from information_schema.columns  where table_name='"+table_name+"'"
    db = getDb()
    cursor = db.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    columns = []
    if data_list:
        for column_detail in data_list:
            for (k, v) in column_detail.items():
                columns.append(v)
    return columns


def update_execute(sql):
    db = getDb()
    cursor = db.cursor()
    update_count = 0
    try:
        update_count = cursor.execute(sql)
        db.commit()
    except UnicodeEncodeError as e:
        db.rollback()
    db.close()
    return update_count
