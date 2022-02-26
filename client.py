from flask import session,render_template, flash ,request, Flask, flash, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.utils import secure_filename
import shutil
import json
import urllib.request
#from appium import webdriver
import time
from datetime import date,datetime
import subprocess
import os
import logging
import threading
import multiprocessing


app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/lambdabd2'

#db= SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'jar'}
#app.config['UPLOAD_FOLDER'] = 'C://Users//Administrator//Desktop//stage'



#DEFINITION DU MODELE(BASE DE DONNEES)


#db.create_all()



#EXECUTION DES SCRIPTS DE TESTS



# PAGE D'ACCUEIL
#---------------
@app.route("/",methods=['GET','POST'])
def index():

    return render_template("index.html")





if __name__ == '__main__':
    app.run()