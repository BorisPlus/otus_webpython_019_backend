import datetime
import json
import os
import sys

from flask import (
    render_template,
    make_response,
    redirect,
    flash,
    url_for,
    request
)
from flask_cors import cross_origin

app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_path not in sys.path:
    sys.path.append(app_path)

from bug_report.config import (
    app,
    db_file,
    app_name,
    app_base_path,
    db
)
from bug_report.models import BugReport

if not os.path.exists(db_file):
    db.create_all()


@app.route("/")
@app.route("/list")
def objects_list():
    return render_template('list.html', flask_objects=BugReport.query.all())


@app.route("/info/<int:id>")
def object_info(id):
    flask_object = BugReport.query.get(id)
    if flask_object:
        return render_template('info.html', id=id, flask_object=flask_object)
    else:
        flash('Object with ID %s was not found.' % id, 'danger')
        return redirect(url_for('objects_list'))


@app.route("/bug_report/create", methods=['POST'])
@cross_origin()
def create():
    # curl -H "Content-type: application/json" -X POST http://127.0.0.1:8280/create -d '{"message":"Hello Data"}'
    print('cross_origin create')
    print('request.method = ', request.method)
    print('request.json = ', request.json)
    print('json.dumps(request.json) = ', json.dumps(request.json))
    print('request.headers = ', request.headers)
    print('request.args = ', request.args)
    b = BugReport()
    b.request_headers = ': '.join(['{}: {}'.format(header[0], header[1], ) for header in request.headers])
    b.request_args = '; '.join(request.args)
    b.request_json = json.dumps(request.json)
    b.datetime = datetime.datetime.now()
    b.href = request.json.get('href')
    b.selected_text = request.json.get('seletedText')
    b.user_text = request.json.get('userText')
    b.honest = True if request.json.get('honestMarker') else False
    db.session.add(b)
    db.session.commit()
    return redirect(url_for('objects_list'))


@app.route("/about")
def about():
    return "BugReport Backend App. (%s, %s)" % (app_name, app_base_path)


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = '404 Not found'
    return resp


if __name__ == '__main__':
    if not os.path.exists(db_file):
        db.create_all()
    app.run(host='127.0.0.1', port=8280)
