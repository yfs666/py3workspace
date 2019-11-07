from flask import Flask, request, render_template

app = Flask(__name__)

import json

from datetime import date, datetime

import yfs.dbutil.service.MyService as myService


class DateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


@app.route('/dbIndex', methods=['GET', 'POST'])
def db_index():
    return render_template('index.html')


@app.route('/dbExecute', methods=['GET', 'POST'])
def db_execute():
    sqlContent = request.form.get("sqlContent")
    if sqlContent.lstrip().startswith('select'):
        sqlColumnAndData = myService.selectExecute(sqlContent)
        resultDict = {"column": sqlColumnAndData[0], "dataList": sqlColumnAndData[1], "type": "query"}
        return json.dumps(resultDict, cls=DateEncoder)
    else:
        updateCount = myService.update_execute(sqlContent)
        resultDict = {"updateCount": updateCount, "type": "update"}
        return json.dumps(resultDict, cls=DateEncoder)


@app.route('/queryTables', methods=['GET', 'POST'])
def query_tables():
    table_name = request.form.get("tableName")
    tables = myService.query_tables(table_name)
    return json.dumps(tables, cls=DateEncoder)


@app.route('/queryColumns', methods=['GET', 'POST'])
def query_columns():
    table_name = request.form.get("tableName")
    tables = myService.query_columns(table_name)
    return json.dumps(tables, cls=DateEncoder)


if __name__ == '__main__':
    app.run()
