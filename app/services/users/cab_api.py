# -*- coding: utf-8 -*-

# User Api Master

import flask                                        as flask
import flask_wtf                                    as wtf
from flask_login                                    import current_user, login_user
import os                                           as os
from werkzeug.utils                                 import secure_filename

# my modules
from app.services.configs.mcf                       import Config, Database_Config
from app.services.courier.svg                       import SvgMaster
from app.services.courier.jsr                       import JsonMaster


from app.alchemy                                     import session as Session
import app.services.users.usr_api                    as UserMaster
from app.alchemy.models.users                        import User

""" Service User"""

folder = "templates"

blueprint: flask.Blueprint = flask.Blueprint('cabinete_api', __name__, template_folder=folder)    
# courier: Courier = Courier()
Session.global_init(Database_Config.USER)
session = Session.create_session()

def init_blueprint(folder: str=Config.TEMPLATES_FOLDER):
    global blueprint 
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)   

def setTemplateFolder(self, folder="templates"):
    global blueprint
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)

def getBlueprint() -> flask.Blueprint:
    return blueprint


# -----------Routes-----------

@blueprint.route('/me/change', methods=['POST'])
def new_avatar():
    if not UserMaster.is_auntethicated():
        return flask.redirect('/me')
    file = flask.request.files['avatar']
    print(file.__dict__)

    
    file.save("static/images/avatars/" + UserMaster.get_user().login + file.filename.split('.')[-1])

    session = Session.create_session()
    session.query(User).filter(User.id==UserMaster.get_user().id).update(
        {
            "avatar": "static/images/avatars/" + UserMaster.get_user().login + file.filename.split('.')[-1]
        }
    )
    
    session.commit()
    return flask.redirect('/me')

@blueprint.route('/me')
def register():
    if not UserMaster.is_auntethicated():
        return flask.redirect('/')
    
    elif flask.request.method == 'GET':
        headers = {
                "main": "Test Page",
                "brand": SvgMaster.getFullLogo(),
                "menu": JsonMaster.htmlifyFile(
                    "./templates/json-templates/menu.json",
                    {
                        "activated": []
                    } 
                ),
                "user": UserMaster.get_userBar()
        }
        return flask.render_template(
            "general-templates/user.html",
            title="login to oxygen",
            headers=headers,
            user=UserMaster.get_user(),
            adress=flask.request.host
        )
