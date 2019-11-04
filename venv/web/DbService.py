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
        db=database,
        port=port,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
    return db


def selectExecute(sql):
    sql = r"sql"
    db = getDb()
    cursor = db.cursor()
    cursor.execute(sql)
    dataList = cursor.fetchall()
    columnNameList = []
    # columnValueList = []

    if dataList :
        for (k, v) in dataList[1].items():
            columnNameList.append(k)
    return columnNameList, dataList



