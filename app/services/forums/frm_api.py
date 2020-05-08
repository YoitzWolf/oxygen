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
from app.alchemy                                    import session as Session

""" Service User"""

folder = "templates"

blueprint: flask.Blueprint = flask.Blueprint('forum_api', __name__, template_folder=folder)    
# courier: Courier = Courier()
# Session.global_init(Database_Config.FORUM)
# session = Session.create_session()

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
    return flask.render_template(
        "general-templates/basic.html",
        title="oxygen",
        headers=headers
    )


