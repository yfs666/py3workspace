import pymysql
import time
import ply.lex as lex, re
import json


# mysql数据库属性
# host = '192.168.230.138'
# port = 3306
# username = 'root'
# password = '123456'
# database = 'yfs'
# def getDb():
#     db = pymysql.connect(
#         host=host,
#         user=username,
#         passwd=password,
#         db=database,
#         port=port,
#         charset='utf8',
#         cursorclass=pymysql.cursors.DictCursor)
#     return db


def __get_db(database):
    "获取数据库连接，从本地文件中获取配置信息，放置数据库配置在代码中出现"
    f = open("D:\py_database_key.txt", "r")
    database_keys_str = f.read()
    database_keys = database_keys_str.split("\n")
    for database_key_val in database_keys:
        database_key = database_key_val.split("=")[0]
        if database == database_key:
            # 根据配置中的key获取本地文件中的数据，类型是json格式
            database_val_json = database_key_val.split("=")[1]
            database_dict = json.loads(database_val_json)
            db = pymysql.connect(
                host=database_dict["host"],
                user=database_dict["username"],
                passwd=database_dict["password"],
                db=database_dict["database"],
                port=database_dict["port"],
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)
            return db


def selectExecute(database, sql):
    db = __get_db(database)
    cursor = db.cursor()
    cursor.execute(sql)
    dataList = cursor.fetchall()
    columnNameList = []
    if dataList:
        for (k, v) in dataList[0].items():
            columnNameList.append(k)
    return (columnNameList, dataList, extract_table_name_from_sql(sql))


def query_tables(database, table_name):
    db = __get_db(database)
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


def query_columns(database, table_name):
    sql = "select column_name from information_schema.columns  where table_name='" + table_name + "'"
    db = __get_db(database)
    cursor = db.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    columns = []
    if data_list:
        for column_detail in data_list:
            for (k, v) in column_detail.items():
                columns.append(v)
    return columns


def update_execute(database, sql):
    db = __get_db(database)
    cursor = db.cursor()
    update_count = 0
    try:
        update_count = cursor.execute(sql)
        db.commit()
    except UnicodeEncodeError as e:
        db.rollback()
    db.close()
    return update_count


def update_column(database, table_name, column_name, column_value, primary_key, primary_value):
    sql = "update " + table_name + " set " + column_name + "= '" + column_value + "' where " + primary_key + " = '" + primary_value + "'";
    db = __get_db(database)
    cursor = db.cursor()
    update_count = 0
    try:
        update_count = cursor.execute(sql)
        db.commit()
    except UnicodeEncodeError as e:
        db.rollback()
    db.close()
    return update_count


def del_by_id(database, table_name, id):
    "根据id删除数据"
    sql = "delete from " + table_name + " where id = " + id
    db = __get_db(database)
    cursor = db.cursor()
    update_count = 0
    try:
        update_count = cursor.execute(sql)
        db.commit()
    except UnicodeEncodeError as e:
        db.rollback()
    db.close()
    return update_count



def extract_table_name_from_sql(sql_str):
    # remove the /* */ comments
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)

    # remove whole line -- and # comments
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]

    # remove trailing -- and # comments
    q = " ".join([re.split("--|#", line)[0] for line in lines])

    # split on blanks, parens and semicolons
    tokens = re.split(r"[\s)(;]+", q)

    # scan the tokens. if we see a FROM or JOIN, we set the get_next
    # flag, and grab the next one (unless it's SELECT).

    result = set()
    get_next = False
    for token in tokens:
        if get_next:
            if token.lower() not in ["", "select"]:
                result.add(token)
            get_next = False
        get_next = token.lower() in ["from", "join"]
    return result
