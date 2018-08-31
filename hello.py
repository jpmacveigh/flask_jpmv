#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, flash, make_response, session
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "toto"

@app.route('/')
def accueil():
    pseudo_du_visiteur=request.cookies.get("pseudo") # on récupère le pseudo du visiteur
    if pseudo_du_visiteur is not None:
        return "Bonjour. C'est un plaisir de vous revoir, {pseudo}".format(pseudo=pseudo_du_visiteur)
    else:
        reponse=make_response("Bonjour. C'est votre première visite !")
        reponse.set_cookie("pseudo","Luc",max_age=20) # le cookie a une durée de vie de 20 secondes
        return reponse 
    d=datetime.now().isoformat()
    mots=["Bonjour","a","toi","visiteur"]
    return render_template("accueil.html",mots=mots, la_date=d,age="95",dist=4850,nombre=22)

app.config["PERMANENT_SESSION_LIFETIME"]= 20 # la session dure 20 secondes

@app.route('/avec_session',methods=["GET","POST"])
def avec_session():
    
    if "pseudo" in session:
        return "Bonjour. C'est un plaisir de vous revoir, {pseudo}".format(pseudo=session["pseudo"])
    else:
        if request.method == "POST":
            pseudo=request.form["pseudo"]
            session["pseudo"]=pseudo
        return render_template("session.html")
        


@app.context_processor
def passer_titre():
    return dict(titre="Bienvenue les gars !")

@app.context_processor
def passer_aux_templates():
    def formater_distance(dist):
        unit="m"
        if dist >1000:
            dist /=1000.
            unit="Km"
        return u"{0:.2f} {1}".format(dist,unit)
    return dict(format_dist=formater_distance)

@app.template_filter("format_dist")
def formater_distance(dist):
    unit="m"
    if dist >1000:
        dist /=1000.
        unit="Km"
    return u"{0:.2f} {1}".format(dist,unit)


@app.route("/contact",methods=["GET","POST"])
def contact():
    donnees_envoyees_correctes=True
    if request.method == "POST":
        if donnees_envoyees_correctes :
            flash(u"Votre message a bien été envoyé !","succes")
        else:
            flash(u"Erreur dans les données envoyées.","erreur")
    return render_template("contact.html")
    
@app.route("/contact2",methods=["GET","POST"])
def contact2():
    if request.method == "POST":
        return "Vous avez envoyé le message : {msg}".format(msg=request.form["message"])
    return render_template("contact.html")
    
@app.route("/contact3") # on n'autorise pas la méthode POST
def contact3():
    if request.args.get("message") is not None:
        return "Vous avez envoyé le message : {msg}".format(msg=request.args["message"])
    return ('<form action="" method="get"> <input type="text" name="message"/> <input type="submit",value="Envoyer"/> </form>')    


@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method=="POST":
        chaine=u"Vous avez envoyé le fichier : {nom}".format(nom=request.files["uploaded"].filename)
        flash(chaine,"succes")
        fichier = request.files["uploaded"]
        nom_fichier=fichier.filename
        if nom_fichier[-5:] != ".html":
            nom_fichier=secure_filename(nom_fichier)
            flash(u"nom_fichier")
            fichier.save("./uploads/" + nom_fichier)
    return render_template("upload.html")

def est_impair(n):
    if n%2==1:
        return True
    return False
    
app.jinja_env.tests["impair"] = est_impair

    

if __name__ == "__main__":
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)) )
