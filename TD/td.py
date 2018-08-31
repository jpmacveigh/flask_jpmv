#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, abort, redirect, make_response, url_for, render_template, flash, send_from_directory
from PIL import Image
from StringIO import StringIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "TD_jpmv"

@app.route('/')
def index():
    #flash(u"Message TD 1")
    #flash(u"Message TD 2")
    return render_template ("accueil_td.html")
    
@app.route("/view")
def view():
    list=os.listdir("./ups")
    return render_template ("view_all.html", list=list)
    
@app.route("/view/<nom_image>")
def affiche_image(nom_image):
    return send_from_directory("./ups", nom_image, as_attachment=False)
    
@app.route("/up",methods=["GET","POST"])
def upload():
    if request.method=="POST":
        chaine=u"Vous avez tenté d'envoyer le fichier : {nom}".format(nom=request.files["uploaded"].filename)
        flash(chaine)
        fichier = request.files["uploaded"]
        nom_fichier=fichier.filename
        if (nom_fichier[-4:].upper() == ".PNG")or(nom_fichier[-4:].upper() == ".JPG")or(nom_fichier[-5:].upper() == ".JPEG"):
            nom_fichier=secure_filename(nom_fichier)
            fichier.save("./ups/" + nom_fichier)
            flash(u"Le fichier a été sauvegardé dans /ups")
        else :
            flash(u"Les seules extensions autorisées sont png, jpg ou jpeg. Le fichier n'a pas été sauvegardé")
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)) )
