#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
from random import randint
import json
import os
import sys
import shutil
import hashlib
import database as DB


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    cabecera = ""
    
    # Establece el fintro por genero/categoria, si hay
    if 'movieCategory' in request.form and request.form['movieCategory'] != "NONE":
        genre_filter = request.form['movieCategory']
        cabecera = " from category '" + request.form['movieCategory'] + "'"
    else:
        genre_filter = None
    
    # Establece el fintro por nombre, si hay
    if 'movieName' in request.form and request.form['movieName'] != "":
        name_filter = request.form['movieName']
        cabecera = " which contains '" + request.form['movieName'] + "'" + cabecera
    else:
        name_filter = None
    
    # Obtiene la lista de peliculas
    movies = DB.list_movies(name_filter=name_filter, genre_filter=genre_filter)
    
    # Obtiene la lista de generos
    categories = DB.list_genres()
    
    if cabecera == "":
        return render_template('index.html', title="Home", movies=movies, categories=categories)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form and 'password' in request.form:
        userAux = DB.get_user(request.form['username'], request.form['password'])
        if len(userAux) == 1 and userAux[0].username == request.form['username']:
            session['usuario'] = request.form['username']
            session.modified = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', title="Sign In")
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():



















































