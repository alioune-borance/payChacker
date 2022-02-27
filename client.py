#from crypt import methods
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bdpayercheck'
 
db= SQLAlchemy(app)

#ALLOWED_EXTENSIONS = {'jar'}
#app.config['UPLOAD_FOLDER'] = 'C://Users//Administrator//Desktop//stage'



#DEFINITION DU MODELE(BASE DE DONNEES)

class Ged_employee(db.Model):
    """
    Create a table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'ged_employee'

    employee_id = db.Column(db.Integer, primary_key=True)
    employee_email = db.Column(db.String(500),unique=True)
    employeee_password = db.Column(db.String(500),unique=True)
    employee_fullname = db.Column(db.String(500))
    employee_role = db.Column(db.String(500))

    #scenarios = db.relationship('Scenario',backref='integrateur',lazy=True)

    def __repr__(self):
        return '<ged_employee: {}>'.format(self.id)

class Ged_file(db.Model):
    """
    Create a table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'ged_file'

    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(500),unique=True)
    file_type = db.Column(db.String(500),unique=True)
    file_src = db.Column(db.String(500))
    file_account_id = db.Column(db.String(500))

    #scenarios = db.relationship('Scenario',backref='integrateur',lazy=True)

    def __repr__(self):
        return '<ged_employee: {}>'.format(self.id)


db.create_all()



#EXECUTION DES SCRIPTS DE TESTS



# PAGE D'ACCUEIL
#---------------
@app.route("/",methods=['GET','POST'])
def index():
    return render_template("connexion.html")

@app.route("/connexion",methods=['GET','POST'])
def connexion():
    p = request.form.get('email')
    e = Ged_employee.query.filter_by(employee_email=p).first()
    if e != None:
        if (request.form.get('mdp') == e.employeee_password):
            files = Ged_file.query.all()
            return render_template("documents.html",fs=files)

    return "p"

@app.route("/recherche",methods=['GET','POST'])
def recherche():
    if request.method == 'POST':
        r = request.form.get('rech')
        files = Ged_file.query.filter(Ged_file.file_name.like("%"+r+"%"))

    return render_template("documents.html",fs=files)

if __name__ == '__main__':
    app.run()