# -*- coding: utf-8 -*-

# main config file - mcf

# libraries
import flask 										as flask
import os                                           as os

# my modules

class Config():
    SECRET_KEY      =   os.environ.get('SECRET_KEY') or 'errorpassword'
    UPLOAD_FOLDER   =   'images/uploads'
    TEMPLATES_FOLDER =  'general-templates'
    FLASK_ENV       =   "development"
    FLASK_DEBUG     =   1
    DEBUG           =   True

class Database_Config():
    USER = "./static/databases/usr-api.db"
    FORUM = "./static/databases/frm-api.db"
    
    
# custom
#ADDRES            =   '::' #"192.168.1.105"
#PORT              =   8080

def getAddres():  return ADDRES  
def getPort():    return PORT
