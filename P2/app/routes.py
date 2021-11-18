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
from . import database as DB


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
    
    if 'numMovies' in request.form and request.form['numMovies'] != "":
        lim = request.form["numMovies"]
    else:
        lim = 20

    # Obtiene la lista de peliculas
    movies = DB.list_movies(name_filter=name_filter,
                            genre_filter=genre_filter,
                            lim=lim)
    
    # Obtiene la lista de generos
    categories = DB.list_genres()

    # Aniade otra informacion
    if cabecera == "":
        cabecera = None
    else:
        cabecera = "Showing movies" + cabecera + ":"

    aux = {"lim": lim,
           "lastGen": genre_filter,
           "lastName": name_filter}

    return render_template('index.html',
                           title="Home",
                           movies=movies,
                           categories=categories,
                           cabecera=cabecera,
                           aux=aux)
        

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



@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in request.form and \
    'password' in request.form and \
    'firstname' in request.form and \
    'lastname' in request.form and \
    'email' in request.form:
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
                respuesta = DB.create_user(request.form['username'],
                                           request.form['password'],
                                           request.form['firstname'],
                                           request.form['lastname'],
                                           request.form['email'],
                                           request.form['creditCard'])
                # Si hay un error en la BD lo indica
                if respuesta == None:
                    return render_template(
                        'register.html',
                        title='Sign Up',
                        mensaje="Error creating customer")
                # Si el registro se ha completado con exito se redirige
                else:
                    return render_template('login.html',
                                       msg="Now you are registered")
            # Si hay algun campo invalido lo indica
            else:
                return render_template('register.html',
                                       title='Sign Up',
                                       msg=msg)
        # Si el usuario ya existe se redirige
        else:
            return render_template('login.html',
                                   msg="User already exist, try to login:")
    else:
        session['url_origen'] = request.referrer
        session.modified = True
        return render_template('register.html', title="Sign Up")
  

@app.route('/showMovie/<int:movieId>', methods=['GET', 'POST'])
def showMovie(movieId):
    if 'cuantity' in request.form:
        if 'usuario' in session:
            username = session['usuario']

            if request.form['cuantity'] == "":
                quantity = 1
            else:
                quantity = int(request.form['cuantity'])
            DB.add_to_cart(username,
                           request.form["product"],
                           quantity)

    return render_template('detalleMovie.html',
                           movie=DB.get_movie_info(movieId),
                           id=movieId)


@app.route('/cesta', methods=['GET', 'POST'])
def cesta():
    if 'usuario' in session:
        username = session['usuario']
        title="Cesta de " + session['usuario']
    else:
        username = "Anonymous"
        title = "Cesta anonima"

    if 'newCuantity' in request.form:
        DB.mod_orderdetail(session['usuario'],
                         request.form['prodId'],
                         request.form['newCuantity'])

    if 'TermComp' in request.form:
        msg = DB.end_cart(session['usuario'])
    else:
        msg = None

    cart = DB.get_actual_cart(username)
    if cart and len(cart) > 0:
        precioCesta = cart[0]["amount"]
    else:
        precioCesta = 0

    return render_template('cesta.html',
                           title=title,
                           cart=cart,
                           precioCesta=precioCesta,
                           msg=msg)


@app.route('/cuenta', methods=['GET', 'POST'])
def cuenta():
    if 'usuario' in session:
        if 'newbudget' in request.form and request.form['newbudget'] != "":
            DB.add_budget(session['usuario'], request.form['newbudget'])
        return render_template(
            'cuenta.html',
            title="Cuenta",
            datos=DB.get_user_minor_info(session['usuario']),
            historial=DB.get_historial(session['usuario']))
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
