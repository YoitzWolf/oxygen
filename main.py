# -*- coding: utf-8 -*-

# Main File

# libraries                                         what
import flask 										as flask
import flask_wtf 									as wtf
import flask_login 									as flogin
from flask_login 									import current_user, login_user
import os 											as os
from werkzeug.utils 								import secure_filename

# my modules
from app.services.configs.mcf 						import Config, getAddres, getPort
from app.services.courier.svg                       import SvgMaster
from app.services.courier.jsr                       import JsonMaster

import app.services.users.usr_api                   as UserMaster
import app.services.users.cab_api                   as СabineteMaster
import app.services.forums.frm_api                  as ForumMaster
import app.services.forums.tgs_api                  as TagMaster
import app.services.forums.mrk_api                  as MarkdownMaster

# App Init
app = flask.Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def main():
    headers = {
            "main": "Main Page",
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
        "general-templates/basic.html",
        title="oxygen",
        headers=headers
    )

if __name__ == "__main__":
    UserMaster.init_login(app=app)
    app.register_blueprint(UserMaster.blueprint)
    
    app.register_blueprint(ForumMaster.blueprint)
    
    app.register_blueprint(TagMaster.blueprint)
    
    app.register_blueprint(MarkdownMaster.blueprint)
    
    app.register_blueprint(СabineteMaster.blueprint)
    
    app.run(host=getAddres(), port=getPort())