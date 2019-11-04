from flask import Flask, request, render_template

app = Flask(__name__)

import json

from datetime import date, datetime

from web import DbService as db


class DateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


@app.route('/dbIndex', methods=['GET', 'POST'])
def dbIndex():
    return render_template('db_index.html')


@app.route('/dbExecute', methods=['GET', 'POST'])
def dbExecute():
    sqlContent = request.args.get("sqlContent")
    sqlColumnAndData = db.selectExecute(sqlContent)
    resultDict = {"column": sqlColumnAndData[0], "dataList": sqlColumnAndData[1]}
    return json.dumps(resultDict, cls=DateEncoder)


if __name__ == '__main__':
    app.run()
