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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/lambdabd2'

db= SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'jar'}
app.config['UPLOAD_FOLDER'] = 'C://Users//Administrator//Desktop//stage'



#DEFINITION DU MODELE(BASE DE DONNEES)

Threads_Scenarios = db.Table('thread_scenario',
    db.Column('idThread',db.Integer,db.ForeignKey('thread.id')),
    db.Column('idScenario',db.Integer,db.ForeignKey('scenario.id'))
)


class Integrateur(db.Model):
    """
    Create an Integrateur table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'integrateur'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(500),unique=True)
    email = db.Column(db.String(500),unique=True)
    mdp = db.Column(db.String(500))

    scenarios = db.relationship('Scenario',backref='integrateur',lazy=True)

    def __repr__(self):
        return '<integrateur: {}>'.format(self.id)


class Application(db.Model):
    """
    Create an application table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(500),unique=True)
    scenarios = db.relationship('Scenario',backref='application',lazy=True)

    def __repr__(self):
        return '<application: {}>'.format(self.id)



class Scenario(db.Model):
    """
    Create a Scenario table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'scenario'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(500))
    fichier = db.Column(db.String(300))
    critique = db.Column(db.Integer)
    commentaire = db.Column(db.String(100))
    seuil = db.Column(db.String(100))
    maintenance = db.Column(db.Integer)
    activation = db.Column(db.Integer)
    idApplication = db.Column(db.Integer,db.ForeignKey('application.id'),nullable=True)
    idIntegrateur = db.Column(db.Integer,db.ForeignKey('integrateur.id'))

    metrics = db.relationship('Metrics',backref='scenario',lazy=True)
    threads = db.relationship("Thread", secondary="thread_scenario")
    tpsExecs = db.relationship('TpsExec',backref='scenario',lazy=True)
    etatScenarios = db.relationship('EtatScenario',backref='scenario',lazy=True)
    EtatActuel = db.relationship('EtatActuel',backref='scenario',lazy=True)

    def __repr__(self):
        return '<scenario: {}>'.format(self.id)


class Thread(db.Model):
    """
    Create a Thread table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'thread'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text, unique=True)
    idRobot = db.Column(db.Integer,db.ForeignKey('robot.id'))
    idTelephone = db.Column(db.Integer,db.ForeignKey('telephone.id'))

    scenarios = db.relationship("Scenario", secondary="thread_scenario")

    def __repr__(self):
        return '<thread: {}>'.format(self.id)


class EtatScenario(db.Model):
    """
    Create a Scenario table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'etatScenario'

    id = db.Column(db.Integer, primary_key=True)
    etat = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    idScenario = db.Column(db.Integer,db.ForeignKey('scenario.id'))


    def __repr__(self):
        return '<etatScenario: {}>'.format(self.id)


class EtatActuel(db.Model):
    """
    Create a EtatActuel table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'etatActuel'

    id = db.Column(db.Integer, primary_key=True)
    etat = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    idScenario = db.Column(db.Integer,db.ForeignKey('scenario.id'))


    def __repr__(self):
        return '<etatActuel: {}>'.format(self.id)


class TpsExec(db.Model):
    """
    Create a Metrics table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'tpsExec'

    id = db.Column(db.Integer, primary_key=True)
    tps = db.Column(db.Text)
    date = db.Column(db.DateTime)
    etat = db.Column(db.Text)
    idScenario = db.Column(db.Integer,db.ForeignKey('scenario.id'))
    

    def __repr__(self):
        return '<tpsExec: {}>'.format(self.id)


class Metrics(db.Model):
    """
    Create a Metrics table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'metrics'

    id = db.Column(db.Integer, primary_key=True)
    tps_moyen = db.Column(db.String(100))
    disponibilite = db.Column(db.String(100))
    indisponibilite = db.Column(db.String(100))
    performance = db.Column(db.String(100))
    nbreTest = db.Column(db.Text)
    date = db.Column(db.DateTime)

    idScenario = db.Column(db.Integer,db.ForeignKey('scenario.id'))


    def __repr__(self):
        return '<metrics: {}>'.format(self.id)



class Robot(db.Model):
    """
    Create a Robot table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'robot'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(250),unique=True)
    ip = db.Column(db.String(500),unique=True)
    port = db.Column(db.String(500),unique=True)

    threads = db.relationship('Thread',backref='robot',lazy=True)

    def __repr__(self):
        return '<robot: {}>'.format(self.id)


class Telephone(db.Model):
    """
    Create a Telephone table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'telephone'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100),unique=True)
    version = db.Column(db.String(50))
    udid = db.Column(db.String(90),unique=True)

    thread = db.relationship('Thread',backref='telephone',lazy=True)

    def __repr__(self):
        return '<telephone: {}>'.format(self.id)


db.create_all()



#EXECUTION DES SCRIPTS DE TESTS

def execute(fichier):
    scenario = Scenario.query.filter_by(fichier = fichier).first()
    success = False
    tps = 0
    start = time.perf_counter()
    today = date.today()
    dateS = d1 = today.strftime('%d/%m/%Y')
    try:
        subprocess.call(['java','-jar',scenario.fichier])
        success = True
        finish = time.perf_counter()
        tps = finish - start
    except:
        success = False

    perf = Metrics(idScenario=scenario.id,tps=tps,success=success,date=dateS)
    db.session.add(perf)
    db.session.commit()


class MonThread(threading.Thread):
    fini = False
    def __init__(self,fichier):
        threading.Thread.__init__(self)
        self.fichier = fichier
        

    def run(self):            
        scenario = Scenario.query.filter_by(fichier = self.fichier).first()
        th = Thread.query.filter_by(nom='t1').first()
        success = False
        tps = 0
        start = time.perf_counter()
        today = date.today()
        #dateS = d1 = today.strftime('%Y-%m-%d %H:%M:%S')
        dateS = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            result = subprocess.call(['java','-jar',scenario.fichier,'Custom Phone','192.168.160.101:5555','4.4.4','127.0.0.1','4723'])
            success = True
            finish = time.perf_counter()
            tps = finish - start
            if ((tps < 5) or (tps > 70)):
                success=False
            else:
                success=True

        except:
            success = False

        fini = True
        perf = TpsExec(idScenario=scenario.id,tps=tps,date=dateS,etat=success)
        db.session.add(perf)
        db.session.commit()

        etat = EtatActuel.query.filter_by(idScenario=scenario.id).first()
        if etat != None:
            db.session.delete(etat)
            db.session.commit()
        e = EtatActuel(etat=success,date=dateS,idScenario=scenario.id)
        db.session.add(e)
        db.session.commit()

        e1 = EtatScenario(etat=success,date=dateS,idScenario=scenario.id)
        db.session.add(e1)
        db.session.commit()

        #Metrics
        at = TpsExec.query.filter_by(idScenario=scenario.id)
        es = EtatScenario.query.filter_by(idScenario=scenario.id)

        n = at.count()
        tps_total = 0
        for a in at:
            tps_total = tps_total + float(a.tps)

        if (n == 0):
            n=1   
           
        tps_moyen = tps_total / n    

        es1 = EtatScenario.query.filter_by(idScenario=scenario.id).filter_by(etat='1')
        es0 = EtatScenario.query.filter_by(idScenario=scenario.id).filter_by(etat='0')
        disponibilite = es1.count() / es.count() * 100
        indisponibilite = es0.count() / es.count() * 100
        
        met = Metrics.query.filter_by(idScenario=scenario.id).first()
        if met != None:
            db.session.delete(met)
            db.session.commit()

        scenario.seuil = tps_moyen
        db.session.commit()

        m = Metrics(tps_moyen=tps_moyen,disponibilite=disponibilite,indisponibilite=indisponibilite,idScenario=scenario.id,date=dateS,performance=0,nbreTest=n)
        db.session.add(m)
        db.session.commit()


class MesThreads(threading.Thread):
    def __init__(self,nom,fichiers,deviceName,version,udid,ip,port):
        threading.Thread.__init__(self)
        self.fichiers = fichiers
        self.nom = nom
        self.stop = 0
        self.deviceName = deviceName
        self.version = version
        self.udid = udid
        self.ip = ip
        self.port = port


    def run(self):
        while True:  
            if (self.stop == 1):
                break
            for f in self.fichiers:
                scenario = Scenario.query.filter_by(fichier = f).first()
                metric = Metrics.query.filter_by(idScenario=scenario.id)
                success = False
                tps = 0
                start = time.perf_counter()
                today = date.today()
                dateS = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                try:
                    subprocess.call(['java','-jar',scenario.fichier,self.deviceName,self.udid,self.version,self.ip,self.port])
                    success = True
                    finish = time.perf_counter()
                    tps = finish - start
                    if ((tps < 10) or (tps > 25)):
                        success=False
                    else:
                        success=True
                except:
                    success = False

                fini = True
                perf = TpsExec(idScenario=scenario.id,tps=tps,date=dateS,etat=success)
                db.session.add(perf)
                db.session.commit()

                etat = EtatActuel.query.filter_by(idScenario=scenario.id).first()
                if etat != None:
                    db.session.delete(etat)
                    db.session.commit()
                e = EtatActuel(etat=success,date=dateS,idScenario=scenario.id)
                db.session.add(e)
                db.session.commit()

                e1 = EtatScenario(etat=success,date=dateS,idScenario=scenario.id)
                db.session.add(e1)
                db.session.commit()

                #Metrics
                at = TpsExec.query.filter_by(idScenario=scenario.id)
                es = EtatScenario.query.filter_by(idScenario=scenario.id)

                n = at.count()
                tps_total = 0
                for a in at:
                    tps_total = tps_total + float(a.tps)

                if (n == 0):
                    n=1   
                
                tps_moyen = tps_total / n    

                es1 = EtatScenario.query.filter_by(idScenario=scenario.id).filter_by(etat='1')
                es0 = EtatScenario.query.filter_by(idScenario=scenario.id).filter_by(etat='0')
                disponibilite = es1.count() / es.count() * 100
                indisponibilite = es0.count() / es.count() * 100
                
                met = Metrics.query.filter_by(idScenario=scenario.id).first()
                if met != None:
                    db.session.delete(met)
                    db.session.commit()

                scenario.seuil = tps_moyen
                db.session.commit()

                m = Metrics(tps_moyen=tps_moyen,disponibilite=disponibilite,indisponibilite=indisponibilite,idScenario=scenario.id,date=dateS,performance=0,nbreTest=n)
                db.session.add(m)
                db.session.commit()



#INITIALISATION DES THREADS
#--------------------------
def initThreads():
    threads = Thread.query.all()
    threadsL = []
    for t in threads:
        fics = []
        sc = t.scenarios
        for s in sc:
            fics.append(s.fichier)
        m = MesThreads(t.nom,fics,t.telephone.nom,t.telephone.version,t.telephone.udid,t.robot.ip,t.robot.port)
        m.daemon = True

        threadsL.append(m)

    return threadsL

allThreads0 = initThreads()
allThreads = initThreads()
allThreads1 = initThreads()


# PAGE D'ACCUEIL
#---------------
@app.route("/",methods=['GET','POST'])
def index():
    threads = Thread.query.all()
    applications = Application.query.all()
    files = ""
    c=""
    filename = ""
    idThread = ""
    idScenario = ""
    
    if request.method == "POST":
        nom = request.files['jar'].filename.replace('.jar','')
        files = request.files['jar']
        tid = request.form.get('idThread')
        th = Thread.query.get(tid)
        critique = 0
        if (request.form.get('critique') == "critique"):
            critique = 1

        #delete before insert
        mid = ""
        sc = Scenario.query.filter_by(nom=nom+"_t"+str(th.id)).first()
        if sc != None:
            mid = sc.id
            Scenario.query.filter_by(nom=nom+"_t"+str(th.id)).delete()

        if mid != "":
            s = Scenario(id=mid,nom=nom+"_t"+str(th.id),fichier=files.filename,critique=0,seuil=0,maintenance=0,activation=1,idApplication=int(request.form.get('idApplication')))
        else:
            s = Scenario(nom=nom+"_t"+str(th.id),fichier=files.filename,critique=0,seuil=0,maintenance=0,activation=1,idApplication=int(request.form.get('idApplication')))
            s.threads.append(th)
        
        db.session.add(s)
        db.session.commit()

        files.save(files.filename)

    return render_template("index.html",threads=threads,applications=applications)


# PAGE D'ETATS DES SCENARIOS
#---------------------------
@app.route('/results',methods=['GET'])
def results():
    robots = Robot.query.all()
    threads = Thread.query.all()
    etats = EtatActuel.query.all()

    return render_template("results.html",etats=etats,robots=robots,threads=threads)


# PAGE D'ETATS DES SCENARIOS D'UN ROBOT
#--------------------------------------
@app.route('/resultsInRobot/<idRobot>',methods=['GET'])
def resultsInRobot(idRobot):
    robots = Robot.query.all()
    threads = Thread.query.all()

    robot = Robot.query.get(idRobot)
    threads = Thread.query.filter_by(idRobot=robot.id)
    scenarios = list()
    etats = []
    for t in threads:
        for s in t.scenarios:
            scenarios.append(s)
            etat = EtatScenario.query.filter_by(idScenario=s.id).first()
            if etat != None:
                etats.append(etat)

    act1 = robot.nom
    act2 = "..."

    return render_template("resultsInRobot.html",etats=etats,scenarios=scenarios,robots=robots,threads=threads,act1=act1,act2=act2)


#PAGE D'ETATS DES SCENARIOS D'UN THREAD
#--------------------------------------
@app.route('/resultsInThread/<idThread>',methods=['GET'])
def resultsInThread(idThread):
    robots = Robot.query.all()
    threads = Thread.query.all()

    thread = Thread.query.get(idThread)
    scenarios = list()
    etats = []
    for s in thread.scenarios:
        scenarios.append(s)
        etat = EtatScenario.query.filter_by(idScenario=s.id).first()
        if etat != None:
            etats.append(etat)

    act1 = thread.robot.nom
    act2 = thread.nom

    return render_template("resultsInRobot.html",etats=etats,scenarios=scenarios,robots=robots,threads=threads,act1=act1,act2=act2)


# PAGE D'EXECUTION DES SCENARIOS
#-------------------------------
@app.route("/listeScenario",methods=['GET'])
def listeScenario():
    t = ""
    scenarios = Scenario.query.all()
    robots = Robot.query.all()
    threads = Thread.query.all()
    applications = Application.query.all()
    m1 = False

    return render_template("liste.html",scenarios=scenarios,robots=robots,threads=threads,t=t,m1=m1,applications=applications)


# GESTION DES APPLICATIONS
#-------------------------
@app.route("/application",methods=['GET','POST'])
def applications():
    applications = Application.query.all()
    nom = ""
    if request.method == "POST":
        nom = request.form.get('nom')

        a = Application(nom=nom)
        db.session.add(a)
        db.session.commit()

    return render_template("application.html",applications=applications)


# ETAT D'UNE APPLICATION
#-----------------------
@app.route("/application/<id>",methods=['GET','POST'])
def application(id):
    application = Application.query.get(id)

    return render_template("app.html",application=application)


# GESTION DES THREADS
#--------------------
@app.route("/createThread",methods=['GET','POST'])
def createThread():
    threads = Thread.query.all()
    nom = ""
    idTelephone = ""
    idRobot = ""
    telephones = Telephone.query.all()
    robots = Robot.query.all()
    if request.method == "POST":
        nom = request.form.get('nom')
        idTel = request.form.get('idTel')
        idRobot = request.form.get('idRobot')

        t = Thread(nom=nom,idTelephone=idTel,idRobot=idRobot)
        db.session.add(t)
        db.session.commit()

    return render_template("createThread.html",robots=robots,telephones=telephones,threads=threads)


# GESTION DES ROBOTS
#-------------------
@app.route("/createRobot",methods=['GET','POST'])
def createRobot():
    robots = Robot.query.all()
    ip = ""
    port = ""
    if request.method == "POST":
        nom = request.form.get('nom')
        ip = request.form.get('ip')
        port = request.form.get('port')

        r = Robot(nom=nom,ip=ip,port=port)
        db.session.add(r)
        db.session.commit()

    return render_template("createRobot.html",robots=robots)


# GESTION DES TELEPHONES
#-----------------------
@app.route("/createTelephone",methods=['GET','POST'])
def createTelephone():
    telephones = Telephone.query.all()
    nom = ""
    version = ""
    if request.method == "POST":
        nom = request.form.get('nom')
        version = request.form.get('version')
        udid = request.form.get('udid')

        t = Telephone(nom=nom,version=version,udid=udid)
        db.session.add(t)
        db.session.commit()

    return render_template("createTelephone.html",telephones=telephones)


# EXECUTION DE TOUS LES SCENARIOS EN BOUCLE
#------------------------------------------
@app.route("/executeAllI/<exec>",methods=['GET','POST'])
def executeAllI(exec):
    threads = Thread.query.all()
    if exec=="true":
        for t in threads:
            print(t.nom)
            scenarios = Thread.query.get(t.id).scenarios
            fichiers = []
            for s in scenarios:
                fichiers.append(s.fichier)
            
            thread = Thread.query.get(t.id)
            nameOfThread = thread.nom
            for t in allThreads:
                time.sleep(2)
                if (t.nom == nameOfThread):
                    t.start()

        flash('En exécution')

        return redirect("/listeScenario")
    
    else:
        for t in threads:
            print(t.nom)
            scenarios = Thread.query.get(t.id).scenarios
            fichiers = []
            for s in scenarios:
                fichiers.append(s.fichier)
            
            thread = Thread.query.get(t.id)
            nameOfThread = thread.nom
            for t in allThreads:
                time.sleep(2)
                if (t.nom == nameOfThread):
                    t.stop=1
        
        flash('Arrêt de l\'exécution')

        return redirect("/listeScenario")

    return redirect("/listeScenario")


# EXECUTION DES SCENARIOS D'UN ROBOT EN BOUCLE
#---------------------------------------------
@app.route("/executeAllInRobots/<idRobot>/<exec>",methods=['GET','POST'])
def executeAllInRobots(idRobot,exec):
    threads = Thread.query.filter_by(idRobot=idRobot).all()
    if exec=="true":
        for t in threads:
            print(t.nom)
            scenarios = Thread.query.get(t.id).scenarios
            fichiers = []
            for s in scenarios:
                fichiers.append(s.fichier)
            
            thread = Thread.query.get(t.id)
            nameOfThread = thread.nom
            for t in allThreads:
                time.sleep(2)
                if (t.nom == nameOfThread):
                    t.start()

        flash('En exécution')


        return redirect("/listeScenario")
    
    else:
        for t in threads:
            print(t.nom)
            scenarios = Thread.query.get(t.id).scenarios
            fichiers = []
            for s in scenarios:
                fichiers.append(s.fichier)
            
            thread = Thread.query.get(t.id)
            nameOfThread = thread.nom
            for t in allThreads:
                time.sleep(2)
                if (t.nom == nameOfThread):
                    t.stop=1
        
        flash('Arrêt de l\'exécution')

        return redirect("/listeScenario")

    return redirect("/listeScenario")


# EXECUTION DES SCENARIOS D'UN THREAD EN BOUCLE
#----------------------------------------------
@app.route("/executeAllInThreads/<idThread>/<exec>",methods=['GET','POST'])
def executeAllInThreads(idThread,exec):
    allThreads5 = initThreads()
    if exec=="true":
        scenarios = Thread.query.get(idThread).scenarios
        fichiers = []
        for s in scenarios:
            fichiers.append(s.fichier)
            
        thread = Thread.query.get(idThread)
        nameOfThread = thread.nom
        
        for t in allThreads1:
            time.sleep(2)
            if (t.nom == nameOfThread):
                t.start()


        flash('En exécution')

        return redirect("/thread/"+idThread)
    
    else:
        scenarios = Thread.query.get(idThread).scenarios
        fichiers = []
        for s in scenarios:
            fichiers.append(s.fichier)
            
        thread = Thread.query.get(idThread)
        nameOfThread = thread.nom
        for t in allThreads1:
            time.sleep(2)
            if (t.nom == nameOfThread):
                t.stop=1
                
        flash('Arrêt de l\'exécution')

        return redirect("/thread/"+idThread)

    return redirect("/thread/"+idThread)



    # thread = Thread.query.get(idThread)
    # threads = Thread.query.all()
    # th = None
    # nameOfThread = thread.nom
    
    # scenarios = Thread.query.get(idThread).scenarios
    # fichiers = []
    # for s in scenarios:
    #     fichiers.append(s.fichier)

    # fics = []
    # for t in threads:
    #     time.sleep(3)
    #     sc = t.scenarios
    #     for s in sc:
    #         fics.append(s.fichier)

    #     if (t.nom == nameOfThread):
    #         th = MesThreads(t.nom,fics)


    # if exec == "false":
    #     th.stop = 1
    # else:
    #     th.start()
        
    # return redirect("/listeScenario")


# EXECUTION D'UN SCENARIO
#------------------------
@app.route("/execute/<string:fichier>")
def execute(fichier):
    # scenario = Scenario.query.filter_by(fichier = fichier).first()
    # success = False
    # tps = 0
    # start = time.perf_counter()
    # today = date.today()
    # dateS = d1 = today.strftime('%d/%m/%Y')
    # try:
    #     subprocess.call(['java','-jar',scenario.fichier])
    #     success = True
    #     finish = time.perf_counter()
    #     tps = finish - start
    # except:
    #     success = False

    # perf = Metrics(idScenario=scenario.id,tps=tps,success=success,date=dateS)
    # db.session.add(perf)
    # db.session.commit()
    #format = "%(asctime)s: %(message)s"
    #logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    #x = threading.Thread(target = execute,args=(fichier,))
    #x.start()
    s = Scenario.query.filter_by(fichier=fichier).first()
    tid = str(s.threads[0].id)
    m = MonThread(fichier)
    m.daemon = True
    m.start()

    flash('En exécution')
    
    
    

    return redirect('/thread/'+tid)


# EXECUTION DE TOUS LES SCENARIOS UNE SEULE FOIS
#----------------------------------------------
@app.route("/executeAll")
def executeAll():
    th = Thread.query.all()
    allThreadId = []
    for t in th:
        allThreadId.append(t.id)

    startG = time.perf_counter()
    for idThread in allThreadId:
        scenarios = Thread.query.get(idThread).scenarios
        fichiers = []
        for s in scenarios:
            fichiers.append(s.fichier)
        
        thread = Thread.query.get(idThread)
        nameOfThread = thread.nom
        for t in allThreads:
            if (t.nom == nameOfThread):
                t.start()
            time.sleep(100)


    tpsG = time.perf_counter() - startG
    print(tpsG)

    return redirect("/listeScenario")


#  AFFICHER LES SCENARIOS D'UN THREAD
#----------------------------------------------
@app.route("/thread/<idThread>")
def thread(idThread):
    t = Thread.query.get(idThread)
    scenarios = Scenario.query.all()
    robots = Robot.query.all()
    threads = Thread.query.all()

    return render_template("liste.html",t=t,scenarios=scenarios,robots=robots,threads=threads)


# AFFICHER LES STATISTIQUES ET METRICS D'UN SCENARIO
#----------------------------------------------------
@app.route("/detailExec/<string:fichier>")
def detailExec(fichier):
    scenario = Scenario.query.filter_by(fichier = fichier).first()
    tpsExec = TpsExec.query.filter_by(idScenario = scenario.id).all()
    metrics = Metrics.query.filter_by(idScenario = scenario.id).first()

    mes = []
    for m in tpsExec:
        mes.append(m.tps)

    n = TpsExec.query.filter_by(idScenario = scenario.id).count()

    return render_template("detailExec.html",metrics=metrics,tpsExec=tpsExec,scenario=scenario,mes=mes,n=n)


if __name__ == '__main__':
    app.run()