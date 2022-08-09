import workdb
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
db = workdb.SelectDatabase()


def do_none(req):
    if not req:
        return None
    else:
        return req


def to_dict(data, count):
    return {
        '#': count + 1,
        'writing_utc': str(data[1]),
        'date_time': str(data[2]),
        'host': data[3],
        'version': data[4],
        'device_vendor': data[5],
        'device_product': data[6],
        'device_version': data[7],
        'signature_id': data[8],
        'name': data[9],
        'severity': data[10],
        'extension': data[11],
        'original_message': data[12]
    }


def last_time(lasttime):
    if lasttime == 1:
        return datetime.now() - timedelta(minutes=10)
    if lasttime == 2:
        return datetime.now() - timedelta(minutes=30)
    if lasttime == 3:
        return datetime.now() - timedelta(hours=1)
    if lasttime == 4:
        return datetime.now() - timedelta(days=1)
    if lasttime == 5:
        return datetime.now() - timedelta(days=30)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST" and 'validate' not in request.form:
        time0 = do_none(request.form['time0'])
        time1 = do_none(request.form['time1'])
        message = do_none(request.form['message'])
        if 'lasttime' in request.form:
            lasttime = do_none(request.form['lasttime'])
            time0 = last_time(int(lasttime))
            time1 = datetime.now()
        if time1 and time0 is None:
            time0 = '1970-01-01 00:00:00'
        if time0 and time1 is None:
            time1 = datetime.now()
        result = db.get_info(
            time=[time0, time1],
            message=message
        )
        return jsonify({
            'data': [to_dict(row, count) for count, row in enumerate(result[::-1])],
            'resp_count': len(result),
            'db_count': db.get_count()}
        )
    elif 'validate' in request.form:
        return jsonify({'data': render_template('the_temp.html')})
    else:
        return render_template("index.html")


@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == "POST":
        jsonData = request.form['data']
        nData = json.loads(jsonData)
        with open('download/cef.log', 'w') as file:
            for row in nData:
                file.write(row)
        return send_file('download/cef.log', as_attachment=True)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        dataFile = request.files['loadfile']
        inputData = dataFile.read()
        decData = inputData.decode('UTF-8').splitlines()
        dataArr = []
        for row in decData:
            dataArr.append(row.split('|'))

        return dataFile


if __name__ == "__main__":
    app.run(host="0.0.0.0")
