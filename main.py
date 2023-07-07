import workdb
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import data
from datetime import datetime, timedelta
import json
import re
import os

app = Flask(__name__)
db = workdb.SelectDatabase()

app.secret_key = b'2c061365ae364cc71c178fa6d423fbd71d80c45073870f76d2c6b000bb91d016'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(login):
    try:
        return data.USERS.get(login)
    except:
        return None

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


def read_cert():
    current_directory = os.path.split(os.path.abspath(__file__))[0]
    cert_dir = os.listdir(current_directory + '/cert')
    return [item for item in cert_dir if '.crt' in item][0]

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
       if request.form["login"]:
           login = request.form["login"]
           password = request.form["password"]
           response = data.confirmUserLogin(login, password)
           if response["status"] == True:
               login_user(data.USERS[login])
               flash(response["message"])
               return redirect(url_for('index'))
           else:
               flash(response["message"])
               return redirect(url_for('login'))
    
    elif request.method == "GET":
        return render_template("login.html")

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
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


if __name__ == "__main__":
    app.run(ssl_context=('./cert/' + read_cert(), './cert/device.key'), host="0.0.0.0")
