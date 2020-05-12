# -*- coding: utf-8 -*-

# User Api Master

import flask 										as flask
import flask_wtf 									as wtf
import flask_login 									as flogin
from flask_login 									import current_user, login_user
import os 											as os
from werkzeug.utils 								import secure_filename

# my modules
from app.services.configs.mcf 						import Config, Database_Config
from app.services.courier.svg                       import SvgMaster
from app.services.courier.jsr                       import JsonMaster

import app.services.users.usr_api                   as UserMaster
import app.services.forums.mrk_api                  as MarkMaster
from app.services.forums.tgs_api                    import getListTags
from app.alchemy                                    import session as Session
from app.alchemy.models.discussions                 import Discussion
from app.alchemy.models.answers                     import Answer

""" Service Forum """

folder = "templates"

blueprint: flask.Blueprint = flask.Blueprint('forum_api', __name__, template_folder=folder)    
# courier: Courier = Courier()
# Session.global_init(Database_Config.FORUM)
session = Session.create_session()

def init_blueprint(folder: str=Config.TEMPLATES_FOLDER):
    global blueprint 
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)   

def setTemplateFolder(self, folder="templates"):
    global blueprint
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)    

def getBlueprint() -> flask.Blueprint:
    return blueprint


@blueprint.route("/forum")
def main():
    headers = {
            "main": "Forum",
            "brand": SvgMaster.getFullLogo(),
            "menu": JsonMaster.htmlifyFile(
                "./templates/json-templates/menu.json",
                {
                    "activated": ["forum"]
                } 
            ),
            "user": UserMaster.get_userBar()
    }
    
    forum = list(session.query(Discussion).all())[::-1];
    
    forum = list(map(lambda x: x.to_dict_beauty(), forum))
    
    return flask.render_template(
        "general-templates/forum.html",
        title="oxygen forum",
        headers=headers,
        tags=getListTags(),
        forum=forum
    )

def get_discuss_html_by_id(did:int):
    discuss = session.query(Discussion).filter(Discussion.id == did).first()
    return flask.render_template("block-templates/discussion.html", discuss=discuss)

def get_discussions(did:list) -> list:
    res = []
    for item in did:
        discuss = session.query(Discussion).filter(Discussion.id == item.id).first()
        res.append(flask.render_template("block-templates/discussion.html", discuss=discuss.to_dict_beauty()))
    return res


@blueprint.route("/forum/search/<header>", methods=["GET", "POST"])
def search(header:str):
  
    forum = list(session.query(Discussion).filter(Discussion.header.like(f'%{header}%')).all())[::-1];
    
    # forum = list(map(lambda x: x.to_dict_beauty(), forum))
    
    forum = get_discussions(forum)
    
    return {"data":forum}

@blueprint.route("/forum/search", methods=["GET", "POST"])
def searchall():

    forum = list(session.query(Discussion).all())[::-1];
    
    # forum = list(map(lambda x: x.to_dict_beauty(), forum))
    
    forum = get_discussions(forum)
    
    return {"data":forum}


@blueprint.route("/forum/d/<id>")
def disc(id:int):
    headers = {
            "main": "Forum",
            "brand": SvgMaster.getFullLogo(),
            "menu": JsonMaster.htmlifyFile(
                "./templates/json-templates/menu.json",
                {
                    "activated": ["forum"]
                } 
            ),
            "user": UserMaster.get_userBar()
    }
    
    discussion = session.query(Discussion).filter(Discussion.id==id).first()
    
    return flask.render_template(
        "general-templates/discussion.html",
        title="oxygen forum",
        headers=headers,
        tags=discussion.tagsfilter(getListTags()),
        answers=map(lambda x: {
                "date":x.getBeautifulDate(), 'author': x.get_author_field(), 'text': MarkMaster.markdown_to_html(data=x.text)}, discussion.answers),
        discussion=discussion.to_dict_beauty(),
        markdown=MarkMaster.markdown_file_to_html(discussion.get_mrk_file())
    )

@blueprint.route("/forum/d/<id>/add", methods=['post'])
def add_answer(id:int):
    if not UserMaster.is_auntethicated():
        return "NO"
    
    data = flask.request.json
    print(data)
    session = Session.create_session()
    discussion = session.query(Discussion).filter(Discussion.id==id).first()
    
    ans = Answer()
    ans.text = data['markdown']
    ans.discussion_id = discussion.id
    ans.author_id = UserMaster.get_user().id
    
    
    session.add(ans)
    session.commit()
    
    return "OK"


@blueprint.route("/forum/new", methods=["GET", "POST"])
def new():
    if not UserMaster.is_auntethicated():
        return flask.redirect("/login")
    elif flask.request.method == 'GET':
        headers = {
                "main": "New Discussion",
                "brand": SvgMaster.getFullLogo(),
                "menu": JsonMaster.htmlifyFile(
                    "./templates/json-templates/menu.json",
                    {
                        "activated": ["forum"]
                    } 
                ),
                "user": UserMaster.get_userBar()
        }
        return flask.render_template(
            "general-templates/new-discussion.html",
            title=headers['main'],
            headers=headers
        )
    elif flask.request.method == 'POST':
        data = flask.request.json
        disc = Discussion()
        disc.author_id =  UserMaster.get_user().id
        disc.header = data['header']
        
        session = Session.create_session()
        session.add(disc)
        disc = session.query(Discussion).filter(Discussion.header==data['header'], Discussion.author_id==UserMaster.get_user().id).all()[-1]
        disc.init_file()
        disc.set_file(data)
        session.query(Discussion).filter(Discussion.id==disc.id).update(disc.to_dict())
        session.commit()
    return "end"
        
        


