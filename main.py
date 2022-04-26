import workdb
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
db = workdb.SelectDatabase()


def do_none(req):
    if not req:
        return None
    else:
        return req


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
            'data': render_template('the_temp.html', result=result),
            'resp_count': len(result),
            'db_count': db.get_count()}
        )
    elif 'validate' in request.form:
        return jsonify({'data': render_template('the_temp.html')})
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
