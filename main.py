import workdb
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
from flask_cors import CORS
import json
import re

app = Flask(__name__)
db = workdb.SelectDatabase()
CORS(app)


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
        'original_message': data[12],
        'id': data[0]
    }


def to_proc_dict(data):
    return {
        'id': data[0],
        'processed_id': data[1],
        'severity': data[2],
        'device_id': data[3]
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
    if request.method == "POST" and 'select_processed' in request.form:
        return jsonify({'data': [to_proc_dict(row) for row in db.get_info(select_proc=True)]})

    if request.method == "POST" and 'processed_id' in request.form:
        processed_id = request.form['processed_id']
        severity = request.form['severity']
        device_id = request.form['device_id']
        db.insert_processed_data([processed_id, severity, device_id])
        return jsonify({'result': 'ok'})

    if request.method == "POST" and 'count_severity' and 'processed' in request.form:
        return jsonify({
            'severity': [
                db.get_count(severity=4) - db.get_count(severity=4, processed=True),
                db.get_count(severity=3) - db.get_count(severity=3, processed=True),
                db.get_count(severity=2) - db.get_count(severity=2, processed=True),
                db.get_count(severity=1) - db.get_count(severity=1, processed=True)
            ]
        })

    if request.method == "POST" and 'validate' not in request.form:
        time0 = do_none(request.form['time0'])
        time1 = do_none(request.form['time1'])
        message = do_none(request.form['message'])
        lastrec = None
        dwnldreq = None
        if 'dwnldreq' in request.form:
            dwnldreq = do_none(request.form['dwnldreq'])
        if 'lasttime' in request.form:
            lasttime = do_none(request.form['lasttime'])
            if lasttime is not None:
                if int(lasttime) == 6:
                    lastrec = 100
                else:
                    time0 = last_time(int(lasttime))
                    time1 = datetime.now()
        if time1 and time0 is None:
            time0 = '1970-01-01 00:00:00'
        if time0 and time1 is None:
            time1 = datetime.now()
        result = db.get_info(
            time=[time0, time1],
            message=message,
            lastrec=lastrec,
            dwnldreq=dwnldreq
        )
        return jsonify({
            'data': [to_dict(row, count) for count, row in enumerate(result[::-1])],
            'resp_count': len(result),
            'db_count': db.get_count()
        }
        )
    elif 'validate' in request.form:
        return jsonify({'data': render_template('the_temp.html')})
    else:
        return render_template("events.html")


@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == "POST":
        jsonData = request.form['data']
        nData = json.loads(jsonData)
        with open('download/cef.log', 'w') as file:
            for row in nData:
                file.write(row)
        return send_file('download/cef.log', as_attachment=True)


@app.route('/send_imitator', methods=['POST', 'GET'])
def send_imitator():
    if request.method == "POST":
        severity_variables = {
            'green': 1,
            'yellow': 2,
            'orange': 3,
            'red': 4
        }
        if request.json['device_severity'] in severity_variables:
            reqSeverity = severity_variables[request.json['device_severity']]
        reqDeviceId, reqDeviceSRA, reqDeviceSRD, reqDeviceName = request.json['device_select'].split(' _')
        dataArr = [(
            datetime.now(),
            datetime.now(),
            'IDS',
            0,
            'OOO SFERA',
            'IDS NET',
            '1.0',
            '1:2101411:13',
            'GPL SNMP public access udp',
            reqSeverity,
            'rt=' + datetime.now().strftime('%b %d %Y %H:%M:%S.%f') +
            ' +0300 cn1=-1347478879 cn1Label=alert '
            'src=10.145.9.125 spt=61292 '
            'dst=172.21.172.233 dpt=161 proto=UDP device_id={0} s_ra={1} s_rd={2} device_name={3}'.format(
                reqDeviceId,
                reqDeviceSRA,
                reqDeviceSRD,
                reqDeviceName
            ),
            datetime.now().strftime('%b %d %Y %H:%M:%S') +
            ' IDS CEF:0|OOO SFERA|IDSnet|1.0|1:2101411:13|GPL SNMP '
            'public access udp|' + str(reqSeverity) + '| ' +
            'device_id={0} device_parent={1} s_ra={1} s_rd={2} device_name={3}'.format(
                reqDeviceId,
                reqDeviceSRA,
                reqDeviceSRD,
                reqDeviceName
            )
        )]
        db.insert_info(dataArr)
        return jsonify({'data': 'its okay'})


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        dataFile = request.files['loadfile']
        inputData = dataFile.read()
        decData = inputData.decode('UTF-8').splitlines()
        dataArr = []
        for row in decData:
            row = row[:-1]
            tempArr = row.split('|')
            date_time, host, version = tempArr[0].rsplit(' ', 2)
            _, version = version.split(':')
            wr_t = re.findall(r'wr_t=(\w{3}\s\d{2}\s\d{4}\s\d{2}:\d{2}:\d{2}\.\d{4,6})', tempArr[7])
            dataArr.append((
                datetime.strptime(wr_t[0], '%b %d %Y %H:%M:%S.%f'),
                datetime.strptime(date_time, '%b %d %Y %H:%M:%S'),
                host,
                version,
                tempArr[1],
                tempArr[2],
                tempArr[3],
                tempArr[4],
                tempArr[5],
                tempArr[6],
                tempArr[7],
                row
            ))
        db.insert_info(dataArr)
        return jsonify({'data': 'Its okey'})


@app.route('/count', methods=['POST', 'GET'])
def count():
    if request.method == "POST":
        return jsonify({'data': db.get_count()})


@app.route('/change_table', methods=['POST', 'GET'])
def change_table():
    if request.method == "POST":
        db.table_name = request.form['table_name']
        return jsonify({'response': 'its okay'})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
