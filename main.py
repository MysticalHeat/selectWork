import workdb
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)
database = workdb.SelectDatabase()


def do_none(req):
    if not req:
        return None
    else:
        return req


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        time0 = do_none(request.form['time0'])
        time1 = do_none(request.form['time1'])
        source_id0 = do_none(request.form['source_id0'])
        source_id1 = do_none(request.form['source_id1'])
        priority = do_none(request.form['priority'])
        weight0 = do_none(request.form['weight0'])
        weight1 = do_none(request.form['weight1'])
        keyword = do_none(request.form['keyword'])
        if source_id1 and source_id0 is None:
            source_id0 = 0
        if source_id0 and source_id1 is None:
            source_id1 = 999
        if weight1 and weight0 is None:
            weight0 = 0
        if weight0 and weight1 is None:
            weight1 = 999
        if time1 and time0 is None:
            time0 = '1970-01-01 00:00:00'
        if time0 and time1 is None:
            time1 = datetime.utcnow()
        result = database.get_info(
            time=[time0, time1],
            source_id=[source_id0, source_id1],
            priority=priority,
            weight=[weight0, weight1],
            keyword=keyword
        )
        return render_template("index.html", result=result)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
