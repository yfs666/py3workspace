from flask import Flask, request, render_template

app = Flask(__name__)

import json
import decimal

from datetime import date, datetime

import yfs.dbutil.service.MyService as myService


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, decimal.Decimal):
            return float(o)
        else:
            return json.JSONEncoder.default(self, o)



@app.route('/index', methods=['GET', 'POST'])
def db_index():
    database = request.args.get("database")
    return render_template('index.html')


@app.route('/dbExecute', methods=['GET', 'POST'])
def db_execute():
    sqlContent = request.form.get("sqlContent")
    database = request.form.get("database")
    if sqlContent.lstrip().startswith('select'):
        sqlColumnAndData = myService.selectExecute(database, sqlContent)
        result_dict = {"column": sqlColumnAndData[0], "dataList": sqlColumnAndData[1], "type": "query",
                       "tableName": sqlColumnAndData[2].pop()}
        return json.dumps(result_dict, cls=MyEncoder)
    else:
        update_count = myService.update_execute(database, sqlContent)
        result_dict = {"updateCount": update_count, "type": "update"}
        return json.dumps(result_dict, cls=MyEncoder)


@app.route('/queryTables', methods=['GET', 'POST'])
def query_tables():
    table_name = request.form.get("tableName")
    database = request.form.get("database")
    tables = myService.query_tables(database, table_name)
    return json.dumps(tables, cls=MyEncoder)


@app.route('/queryColumns', methods=['GET', 'POST'])
def query_columns():
    table_name = request.form.get("tableName")
    database = request.form.get("database")
    tables = myService.query_columns(database,table_name)
    return json.dumps(tables, cls=MyEncoder)


@app.route('/updateColumn', methods=['GET', 'POST'])
def update_column():
    table_name = request.form.get("tableName")
    column_name = request.form.get("columnName")
    column_value = request.form.get("columnValue")
    primary_key = request.form.get("primaryKey")
    primary_value = request.form.get("primaryValue")
    database = request.form.get("database")
    update_count = myService.update_column(database, table_name, column_name, column_value, primary_key, primary_value)
    result_dict = {"updateCount": update_count, "type": "update_column"}
    return json.dumps(result_dict, cls=MyEncoder)



@app.route('/delById', methods=['GET', 'POST'])
def del_by_id():
    database = request.form.get("database")
    table_name = request.form.get("tableName")
    id = request.form.get("id")

    update_count = myService.del_by_id(database, table_name, id)
    result_dict = {"updateCount": update_count, "type": "del_by_id"}
    return json.dumps(result_dict, cls=MyEncoder)


if __name__ == '__main__':
    app.run()
