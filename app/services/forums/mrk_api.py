import flask 										as flask
import flask_wtf 									as wtf
import flask_login 									as flogin
from flask_login 									import current_user, login_user
import os 											as os
import markdown

folder = "templates/markdown"

blueprint: flask.Blueprint = flask.Blueprint('mark_api', __name__, template_folder=folder) 

@blueprint.route('/markdown/file/<string:filename>')
def markdown_file_to_html(filename):
    # markdown file to html
    f = open(filename, 'r')
    data = f.read()
    print(data)
    html = markdown_to_html(data.replace('"', " "))
    return html

@blueprint.route('/markdown/convert', methods=["GET", "POST"])
def markdown_to_html(data=None):
    # markdown to html
    if data is None:
        data = flask.request.json["data"]
        print(flask.request.json)
    return markdown.markdown(data, extensions=['codehilite'])