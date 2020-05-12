# -*- coding: utf-8 -*-

# User Api Master

import flask 										as flask
import flask_wtf 									as wtf
import flask_login 									as flogin
from flask_login 									import current_user, login_user
import os 											as os
from werkzeug.utils 								import secure_filename
import sqlalchemy

# my modules
from app.services.configs.mcf 						import Config, Database_Config
from app.services.courier.svg                       import SvgMaster
from app.services.courier.jsr                       import JsonMaster

import app.services.users.usr_api                   as UserMaster

from app.alchemy                                    import session as Session
from app.alchemy.models.tags                        import Tag
from app.alchemy.models.users                       import User


""" Service Tags"""

folder = "templates"

blueprint: flask.Blueprint = flask.Blueprint('tag_api', __name__, template_folder=folder)    
# courier: Courier = Courier()
# Session.global_init(Database_Config.FORUM)
session = Session.create_session()

def getListTags():
    return list(map(lambda x: x.to_dict(), session.query(Tag).all()))

def init_blueprint(folder: str=Config.TEMPLATES_FOLDER):
    global blueprint 
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)   

def setTemplateFolder(self, folder="templates"):
    global blueprint
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)    

def getBlueprint() -> flask.Blueprint:
    return blueprint


@blueprint.route("/tags")
def main():
    headers = {
            "main": "Forum",
            "brand": SvgMaster.getFullLogo(),
            "menu": JsonMaster.htmlifyFile(
                "./templates/json-templates/menu.json",
                {
                    "activated": ["tags"]
                } 
            ),
            "user": UserMaster.get_userBar()
    }
    
    all_tags = session.query(Tag).all()
    
    print(all_tags)
    return flask.render_template(
        "general-templates/tags.html",
        title="oxygen",
        headers=headers,
        tags=all_tags
    )

@blueprint.route("/tags/search/<string:tag>", methods=["GET", "POST"])
def search(tag:str):
    if tag is None or len(tag)==0: 
        return {'status': True, 'tags': list(map(lambda x: x.to_dict(), session.query(Tag).all()))}
    res = list(session.query(Tag).filter(Tag.header.like(f"%{tag}%")))
    # print(f"%{tag}%")
    return {'status': (len(res) != 0), 'tags': list(map(lambda x: x.to_dict(), res))}


@blueprint.route("/tags/search/", methods=["GET", "POST"])
def search_all():
    return {'status': True, 'tags': list(map(lambda x: x.to_dict(), session.query(Tag).all()))}


@blueprint.route("/tags/check-unique/<string:tag>", methods=["GET", "POST"])
def check_unique(tag:str):
    return 'unic' if session.query(Tag).filter(Tag.header==tag.lower()).first() is None else 'ununic'


@blueprint.route("/tags/new", methods=["GET", "POST"])
def new(*args, **kwargs):
    if not UserMaster.is_auntethicated():
        return "/login"
    
    req = flask.request.json
    
    tag = Tag()
    tag.header = req['header']
    tag.color = req['color']
    tag.bg_color = req['bg_color']
    tag.author_id = UserMaster.get_user().id
    
    session = Session.create_session()
    session.add(tag)
    session.commit()
    
    
    return "/tags"

