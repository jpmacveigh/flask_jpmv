#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, abort, redirect, make_response, url_for
from PIL import Image
from StringIO import StringIO


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello JPMV world !"

@app.route('/racine/')
def racine():
    return "Le chemin de 'racine' est : " + request.path

@app.route('/racine/la')
def racine_la():
    return "Le chemin de 'racine/la' est : " + request.path
    

@app.route('/salut/<monami>')
def salut(monami):
    return "<h2>Bonjour %s </h2>" % monami
    
@app.route('/nombre/<int:n>')
def nombre(n):
    moit=n/2
    return "<h2>Nombre = %s sa moitié vaut = %s </h2>" % (n,moit)
    
@app.route('/contact/' ,methods=["GET","POST"])
def contact():
    if (request.method=="GET") :
        mail = "jpmacveigh@hotmail.fr"
        tel = "06 85 54 03 10"
        return "<h2>Mail : {} .... Tel : {} </h2>".format(mail,tel)
    else:
        return "On traite les donnees recues"
        
@app.route ("/discussion/")
@app.route ("/discussion/page/<int:num_page>")
def chat(num_page=1):
    premier=1+50*(num_page-1)
    dernier=premier+50
    return "Affichage des message {} a {}".format(premier, dernier)

@app.route("/image")
def genere_image():
    mon_image=StringIO()
    Image.new("RGB",(300,300),"#92C41D").save(mon_image,"BMP")
    reponse=make_response(mon_image.getvalue())
    reponse.mimetype="image/bmp"  # à la place de "text/html"
    return reponse
    
@app.route("/404")
def page_non_trouvee():
    #reponse=make_response("Cette page doit retourner une erreur 404")
    #reponse.status=404
    #return reponse
    return "Cette page doit retourner une erreur 404",404
    
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def ma_page_error(error):
    return "Ma trés jolie page {}".format(error.code),error.code

@app.route("/profil/<pseudo>")
def profil(pseudo):
    utilisateur_non_identifie = True
    if utilisateur_non_identifie:
        return redirect(url_for("page_de_login",pseudo=pseudo))
    return "vous êtes identifié {}, voici la page demandée ...".format(pseudo)

@app.route ("/login/<pseudo>")
def page_de_login(pseudo):
    return "vous devez vous connecter {} pour accéder à la page demandée".format(pseudo)

@app.route("/Google")
def redirection_google():
    return redirect("http://www.google.fr")

if __name__ == "__main__":
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)) )
