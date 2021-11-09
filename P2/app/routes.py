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
    
    # Establece el filtro por genero/categoria, si hay
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
    if 'username' in request.form and 'password' in request.form:
        # Busca al usuario que encaje con el username y password
        userAux = DB.get_user(request.form['username'], request.form['password'])
        # Comprueba que exista una coincidencia
        if len(userAux) == 1 and userAux[0].username == request.form['username']:
            # Actualiza la sesion
            session['usuario'] = request.form['username']
            session.modified = True
            # Vuelve al index
            return redirect(url_for('index'))
        # Si no hay coincidencias muestra un error
        else:
            return render_template('login.html',
                                   msg="Username and Password didn't match")
    else:
        session['url_origen']=request.referrer
        session.modified=True        
        print(request.referrer, file=sys.stderr)
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))


"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in request.form and 'password' in request.form and 'email' in request.form and'creditCard' in request.form:
        if DB.username_exists(request.form['username']) == False:
            # Valida los campos introducidos
            validated = True
            msg = {'username': validarNombre(request.form['username']),
                   'password': validarPassword(request.form['password']),
                   'email': validarMail(request.form['email'])}
            for key in msg.keys():
                if msg[key] != "OK":
                    validated = False

            # Si los campos son validos crea al usuario
            if validated == True:
                
            # Si hay algun campo invalido lo indica
            else:
                return render_template('register.html', title='Sign Up', msg=msg)

        else:
            return render_template('login.html',
                                   msg="User already exist, login to continue:")
"""
  

@app.route('/showMovie/<int:movieId>', methods=['GET', 'POST'])
def showMovie(movieId):
    movie = DB.get_movie(movieid)

    if movie == None:
        return render_template('detalleMovie.html', title="Not found")

    if 'cuantity' in request.form and request.form['cuantity'] != "":
        if 'usuario' in session:
            username = session['usuario']
        else:
            username = "ANONYMOUS"
        DB.add_to_cart(username, movieId, int(request.form['cuantity']))

    return render_template('detalleMovie.html', movie=movie, title=movie['titulo'])


@app.route('/cesta', methods=['GET', 'POST'])
def cesta():
    if 'usuario' in session:
        username = session['usuario']
        title="Cesta de " + session['usuario']
    else:
        username = "Anonymous"
        title = "Cesta anonima"

    if 'newCuantity' in request.form:
        DB.mod_ordertail(session['usuario'],
                         request.form['movieId'],
                         request.form['newCuantity'])

    if 'TermComp' in request.form:
        msg = DB.end_cart(session['usuario'])

    cart = DB.get_actual_cart(username)

    return render_template('cesta.html',
                           title=title,
                           cart=cart,
                           precioCesta=cart[0]["OD.totalamount"]
                           mensaje=msg)


@app.route('/cuenta', methods=['GET', 'POST'])
def cuenta():
    if 'usuario' in session:
        historialAux = DB.get_historial(session['usuario'])
        userInfo = DB.get_user_minor_info(session['usuario'])

        return render_template('cuenta.html',
                               title="Cuenta",
                               datos=userInfo,
                               historial=userInfo)
    else:
        return render_template('login.html', title='Sign In')


######## Validaciones ########

def validarNombre(nombre):
    if nombre.find(" ") >= 0:
        return "Username can't contain spaces."
    else:
        return "OK"


def validarPassword(password):
    if password.find(" ") >= 0:
        return "Password can't contain spaces."
    elif len(password) < 8:
        return "Username can't contain less than 8 caracters"
    else:
        return "OK"


def validarMail(mail):
    pos_arroba = mail.find("@")
    pos_punto = mail.find(".")
    
    if pos_arroba < 1 or pos_punto < pos_arroba + 2 or pos_punto == len(mail) - 1:
        return "Incorrect mail format: example@example.example"
    else:
        return "OK"
