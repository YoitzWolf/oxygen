# -*- coding: utf-8 -*-

# User Api Master

import flask                                        as flask
import flask_wtf                                    as wtf
import flask_login                                  as flogin
from flask_login                                    import current_user, login_user
import os                                           as os
from werkzeug.utils                                 import secure_filename

# my modules
from app.services.configs.mcf                       import Config, Database_Config
from app.services.courier.svg                       import SvgMaster
from app.services.courier.jsr                       import JsonMaster


from app.alchemy                                     import session as Session
from app.alchemy.models.users                        import User

""" Service User"""

folder = "templates"

blueprint: flask.Blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)    
login_manager: flogin.LoginManager = flogin.LoginManager()
# courier: Courier = Courier()
Session.global_init(Database_Config.USER)
session = Session.create_session()

def init_blueprint(folder: str=Config.TEMPLATES_FOLDER):
    global blueprint 
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)   

def init_login(app: flask.Flask=None):
    login_manager.setup_app(app)

def setTemplateFolder(self, folder="templates"):
    global blueprint
    blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)    

def setApp(app):
    global login
    login_manager.setup_app(app)

def getBlueprint() -> flask.Blueprint:
    return blueprint

def is_auntethicated():
    return flogin.current_user.is_authenticated

def get_user():
    return flogin.current_user

# -----------API INTERFACE COURIER-----------
def get_userBar():
    if not flogin.current_user.is_authenticated:
        return JsonMaster.htmlifyFile("./templates/json-templates/user-bar.json", {})["unautorised"]
    else:
        return JsonMaster.htmlifyFile(
            "./templates/json-templates/user-bar.json",
            {
                "attr": {
                    "username": flogin.current_user.login,
                    "user-avatar": flogin.current_user.avatar
                }
            }
        )["autorised"]

# -----------Routes-----------

@login_manager.user_loader
def load_user(id):
    return session.query(User).filter( User.id==int(id) ).first()

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if flogin.current_user.is_authenticated:
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
                )        
        }
        return flask.render_template(
            "general-templates/register.html",
            title="login to oxygen",
            headers=headers
        )
    
    elif flask.request.method == 'POST':
        data = flask.request.form   
        flask.flash("POST :: ", data)
        
        user = User()
        user.login = data['login']
        user.email = data['email']
        lst =[
            "./static/images/avatars/av/avatar_00.png",
            "./static/images/avatars/av/avatar_01.png",
            "./static/images/avatars/av/avatar_02.png"
        ]
        from random import choice
        user.avatar = choice(lst)
        
        if(data['password'] == data['password-rep']):
            user.set_password(data['password'])
        else:
            del user
            return "SHIT"
        
        session = Session.create_session()
        session.add(user)
        session.commit()

        return flask.redirect("/login")



@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if flogin.current_user.is_authenticated:
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
                )        
        }
        return flask.render_template(
            "general-templates/login.html",
            title="login to oxygen",
            headers=headers
        )
    elif flask.request.method == 'POST':
        data = flask.request.form
        user = session.query(User).filter( (User.login==data['login']) | ((User.email==data['login']))).first()
        print(user, "entered")
        if user is None or not user.check_password(data['password']):
            flask.flash(f"Invalid username or password: login: {data['login']}")
            return flask.redirect('/login')
        
        login_user(user, remember=True)
        # if not flogin.is_safe_url(next):    return flask.abort(400)
            
        return flask.redirect("/")


@blueprint.route('/logout')
def logout():
    flogin.logout_user()
    return flask.redirect('/')

# ------------------------user pages----------------------


