#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys
from random import randint
import shutil
import hashlib

def slugify(texto):
    return texto.lower().replace(" ", "-")

def leerCatalogue(direccion, nombre_lista):
    catalogue_data = open(os.path.join(app.root_path, direccion), encoding="utf-8").read()
    if catalogue_data:
        catalogue = json.loads(catalogue_data)
        if nombre_lista != "NONE" and nombre_lista in catalogue and len(catalogue[nombre_lista]) > 0:
            for movie in catalogue[nombre_lista]:
                movie['slug_name'] = slugify(movie['titulo'])
        return catalogue
    else:
        catalogue = {}
        catalogue[nombre_lista] = []
        return catalogue

def leerUser(usuario):
    direccion = "usuarios/" + usuario + "/data.dat"
    if os.path.exists("app/" + direccion):
        text = open(os.path.join(app.root_path, direccion), encoding="utf-8").read()
        user = {}
        for duplaAux in text.split(';'):
            dupla = duplaAux.split('=')
            user[dupla[0]] = dupla[1]
        return user
    return None

def escribirUser(usuario, datos):
    if os.path.exists("app/usuarios/" + usuario + "/data.dat"):
        ftpr = open("app/usuarios/" + usuario + "/data.dat", "w")
        ftpr.write("username="+ datos['username'] + ";password=" + datos['password'] + ";email=" + datos['email']
                   + ";creditCard=" + datos['creditCard'] + ";budget=" + datos['budget'])
        ftpr.close()
        
        return

def validarContra(password):
    if password.find(" ") >= 0:
        return "La contrasenia no puede contener espacios en blanco."
    elif len(password) < 8:
        return "La contrasenia no puede tener menos de 8 caracteres."
    else:
        return "ACEPTADA"

def validarMail(mail):
    pos_arroba = mail.find("@")
    pos_punto = mail.find(".")
    
    if pos_arroba < 1 or pos_punto < pos_arroba + 2 or pos_punto == len(mail) - 1:
        return "Formato de mail incorrecto. Formato aceptado: example@example.example"
    else:
        return "ACEPTADA"

def validarNombre(nombre):
    if nombre.find(" ") >= 0:
        return "El nombre no puede contener espacios."
    else:
        return "ACEPTADA"

def getUsernameActual():
    if 'usuario' in session:
        return session['usuario']
    else:
        return "Anonymous"

def modificarEnCesta(slugNameMovie, cantidad):
    username = getUsernameActual()
    
    cesta = leerCatalogue('usuarios/' + username + '/cesta.json', 'cesta')
    
    for movie in cesta['cesta']:
        if movie['slug_name'] == slugNameMovie:
            movie['cantidad'] = cantidad
            break
    
    # Se reescribe el fichero 'cesta.json' con la pelicula modificada
    with open('app/usuarios/' + username + '/cesta.json', 'w') as file:
        json.dump(cesta, file, indent=4)
    
    return

def aniadirACesta(slugNameMovie, cantidad=1):
    username = getUsernameActual()
    
    catalogue = leerCatalogue('catalogue/catalogue.json', 'peliculas')
    cesta = leerCatalogue('usuarios/' + username + '/cesta.json', 'cesta')
    
    # Si la pelicula ya esta en la cesta no se hace nada
    for movie in cesta['cesta']:
        if movie['slug_name'] == slugNameMovie:
            return redirect(url_for('showMovie', slugNameMovie=slugNameMovie))
    
    # Busca la pelicula en el catalogo
    for movie in catalogue['peliculas']:
        if movie['slug_name'] == slugNameMovie:
            # Se aniade la nueva pelicula a la cesta
            movie_cesta = {"id": movie['id'],
                           "titulo": movie['titulo'],
                           "precio": movie['precio'],
                           "cantidad": cantidad}
            cesta['cesta'].append(movie_cesta)
            
            # Se reescribe el fichero 'cesta.json' con la nueva pelicula aniadida
            with open('app/usuarios/' + username + '/cesta.json', 'w') as file:
                json.dump(cesta, file, indent=4)
            
            break
    
    return redirect(url_for('showMovie', slugNameMovie=slugNameMovie))

def terminarCompra():
    username = getUsernameActual()
    
    # Lee la cesta del usuario
    cestaActual = leerCatalogue("usuarios/" + username + "/cesta.json", "cesta")
    catalogo = leerCatalogue("catalogue/catalogue.json", "peliculas")
    
    # Si la cesta esta vacia se indica por pantalla
    if len(cestaActual['cesta']) < 1:
        return "No hay elementos en la cesta para poder comprar."
    
    # Comprueba si los articulos de la cesta siguen estando disponibles en el catalogo
    cestaCorrecta = {}
    cestaCorrecta['cesta'] = []
    algunaEliminada = False
    mensaje = ""
    precioCesta = 0
    for movieCesta in cestaActual['cesta']:
        encontrado = False
        for movieCatalogo in catalogo['peliculas']:
            if movieCesta['slug_name'] == movieCatalogo['slug_name']:
                cestaCorrecta['cesta'].append(movieCesta)
                precioCesta += float(movieCesta['precio']) * int(movieCesta['cantidad'])
                encontrado = True
        # Si alguna pelicula ya no esta disponible se indicara por pantalla
        if encontrado == False:
            if algunaEliminada == False:
                mensaje = "Algunas peliculas de la cesta no estan disponibles. Se intentara continuar con la compra del resto.\n\
                           Peliculas no procesadas y eliminadas:\n"
            mensaje += "    " + movieCesta['titulo'] + "\n"
            algunaEliminada = True
    
    if len(cestaCorrecta['cesta']) < 1:
        # Si no quedan peliculas disponibles se indica por pantalla
        mensaje = "No hay peliculas disponibles para comprar.\n" + mensaje
        
        # Si se han detectado peliculas ya no disponibles si modifica el archivo 'cesta.json'
        if algunaEliminada == True:
            with open("app/usuarios/" + username + "/cesta.json", "w") as file:
                json.dump(cestaCorrecta, file, indent=4)
        
        return mensaje
    
    # Lee los datos del usuario
    dataUsuario = leerUser(username)
    
    # Comprueba que el usuario tenga saldo suficiente
    if float(dataUsuario['budget']) < precioCesta:
        # Si no hay saldo suficiente se indica por pantalla
        mensaje = "SALDO INSUFICIENTE!!! (" + dataUsuario['budget'] + ")\n" + mensaje
        
        # Si se han detectado peliculas ya no disponibles si modifica el archivo 'cesta.json'
        if algunaEliminada == True:
            with open("app/usuarios/" + username + "/cesta.json", "w") as file:
                json.dump(cestaCorrecta, file, indent=4)
        
        return mensaje
    
    # Se le resta el precio de la cesta al saldo del usuario
    dataUsuario['budget'] = str(float(dataUsuario['budget']) - float(precioCesta))
    escribirUser(username, dataUsuario)
    
    # Se aniaden las peliculas compradas al historial
    historial = leerCatalogue("usuarios/" + username + "/historial.json", "historial")
    for movie in cestaCorrecta['cesta']:
        historial['historial'].append(movie)
    with open("app/usuarios/" + username + "/historial.json", "w") as file:
        json.dump(historial, file, indent=4)
    
    # Se vacia la cesta
    with open("app/usuarios/" + username + "/cesta.json", "w") as file:
        cestaAux = {"cesta": []}
        json.dump(cestaAux, file, indent=4)
    
    mensaje = "Compra realizada con exito.\n" + mensaje
    
    return mensaje

####################################################################
####################################################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue = leerCatalogue('catalogue/catalogue.json', 'peliculas')
    movies = []
    valido_aux = False
    cabecera = ""
    categories = []
    
    for movie in catalogue['peliculas']:
        if movie['categoria'] not in categories:
            categories.append(movie['categoria'])
    
    # Se filtra por categoria
    if 'movieCategory' in request.form and request.form['movieCategory'] != "NONE":
        cabecera = " from category '" + request.form['movieCategory'] + "'"
        movies = filter(lambda pelicula: pelicula['categoria'] == request.form['movieCategory'], catalogue['peliculas'])
        valido_aux = True
    else:
        movies = catalogue['peliculas']
    
    # Se filtra por nombre
    if 'movieName' in request.form and request.form['movieName'] != "":
        cabecera = " which contains '" + request.form['movieName'] + "'" + cabecera
        movies = filter(lambda pelicula: pelicula['titulo'].find(request.form['movieName']) >= 0, movies)
        valido_aux = True
    
    if valido_aux == True:
        cabecera = "Movies" + cabecera + ":"
        return render_template('index.html', title="Home", movies=movies, categories=categories, cabecera=cabecera)
    else:
        return render_template('index.html', title="Home", movies=catalogue['peliculas'], categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form and 'password' in request.form:
        if os.path.exists("app/usuarios/" + request.form['username']):
            user = leerUser(request.form['username'])
            contraseniaCifrada = hashlib.sha512((request.form['password']).encode('utf-8')).hexdigest()
            if user['password'] == contraseniaCifrada:
                session['usuario'] = request.form['username']
                session.modified = True
                # se puede usar request.referrer para volver a la pagina desde la que se hizo login
                return redirect(url_for('index'))

                # aqui se le puede pasar como argumento un mensaje de login invalido
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
    if 'username' in request.form and 'password' in request.form and 'email' in request.form and'creditCard' in request.form:
        if os.path.exists("app/usuarios/" + request.form['username']) == True:
            return render_template('login.html', title='Sign In')
        else:
            devuelto = validarContra(request.form['password'])
            if devuelto == "ACEPTADA":
                devuelto = validarMail(request.form['email'])
                if devuelto == "ACEPTADA":
                    devuelto = validarNombre(request.form['username'])
                    if devuelto == "ACEPTADA":
                        
                        contraseniaCifrada = hashlib.sha512((request.form['password']).encode('utf-8')).hexdigest()
                        
                        # Crea la carpeta para el nuevo usuario
                        dir = "app/usuarios/" + request.form['username']
                        os.mkdir(dir)
                        
                        # Crea el archivo data.dat donde se guardara la informacion sobre el nuevo usuario
                        file = (dir + "/data.dat")
                        ftpr = open(file, "w")
                        budget = str(round(randint(0, 100), 2))
                        ftpr.write("username="+ request.form['username'] + ";password=" + contraseniaCifrada + ";email=" + request.form['email']
                               + ";creditCard=" + request.form['creditCard'] + ";budget=" + budget)
                        ftpr.close()
                        
                        # Crea el archivo cesta.json donde se guardara la cesta del nuevo usuario
                        ftpr = open("app/usuarios/" + request.form['username'] + "/cesta.json", "w")
                        ftpr.close()
                        
                        if 'guardarCesta' in request.form:
                            # Copia la cesta anonima actual en la del nuevo usuario
                            shutil.copy("app/usuarios/Anonymous/cesta.json", "app/usuarios/" + request.form['username'] + "/cesta.json")
                            
                            # Borra la cesta anonima
                            ftpr = open("app/usuarios/Anonymous/cesta.json", "w")
                            ftpr.close()
                        
                        # Crea el archivo historial.json donde se guardara el historial del nuevo usuario
                        ftpr = open("app/usuarios/" + request.form['username'] + "/historial.json", "w")
                        ftpr.close()
                        
                        # Se redirige a la pantalla de log in para que el usuario inicie sesion
                        return render_template('login.html', title='Sign In')
            
            # Si no ha cumplido todos los requisitos se recargara la pagina con un mensaje
            return render_template('register.html', title='Sign Up', mensaje=devuelto)
    else:
        # Se puede guardar la pagina desde la que se invoca
        session['url_origen'] = request.referrer
        session.modified = True
        # Print a error.log de Apache si se ejecuta bajo mod_wsgi
        print(request.referrer, file=sys.stderr)
        return render_template('register.html', title="Sign Up")

@app.route('/showMovie/<string:slugNameMovie>', methods=['GET', 'POST'])
def showMovie(slugNameMovie):
    catalogue = leerCatalogue('catalogue/catalogue.json', 'peliculas')
    
    for movie in catalogue['peliculas']:
        if slugify(movie['titulo']) == slugNameMovie:
            if 'cuantity' in request.form and request.form['cuantity'] != "":
                print("Aniadiendo " + request.form['cuantity'] + " a " + slugNameMovie)
                aniadirACesta(slugNameMovie, request.form['cuantity'])
            return render_template('detalleMovie.html', movie=movie, title=movie['titulo'])
    
    return render_template('detalleMovie.html', title="Not found")

@app.route('/cesta', methods=['GET', 'POST'])
def cesta():
    if 'usuario' in session:
        username = session['usuario']
        title="Cesta de " + session['usuario']
    else:
        username = "Anonymous"
        title="Cesta anonima"
    
    # Si se introduce una nueva cantidad se modifican los datos
    if 'newCuantity' in request.form:
        modificarEnCesta(request.form['slugNameMovie'], request.form['newCuantity'])
    
    mensaje = ""
    if 'TermComp' in request.form:
        mensaje = terminarCompra()
    
    cesta_aux = leerCatalogue("usuarios/" + username + "/cesta.json", "cesta")
    catalogue = leerCatalogue("catalogue/catalogue.json", "peliculas")
    
    cesta = []
    precioCesta = 0.0
    for pelicula in catalogue['peliculas']:
        for pelicula_aux in cesta_aux['cesta']:
            if pelicula_aux['id'] == pelicula['id']:
                dupla = {}
                dupla['movie'] = pelicula
                dupla['cuantity'] = pelicula_aux['cantidad']
                cesta.append(dupla)
                precioCesta += float(pelicula['precio']) * int(pelicula_aux['cantidad'])
    
    if mensaje != "":
        return render_template('cesta.html', title=title, catalogue=cesta, precioCesta=precioCesta, mensaje=mensaje)
    else:
        return render_template('cesta.html', title=title, catalogue=cesta, precioCesta=precioCesta)

@app.route('/quitarDeCesta/<string:slugNameMovie>', methods=['GET', 'POST'])
def quitarDeCesta(slugNameMovie):
    username = getUsernameActual()
    
    cesta = leerCatalogue('usuarios/' + username + '/cesta.json', 'cesta')
    
    nuevaCesta = {}
    peliculas = []
    for movie in cesta['cesta']:
        if movie['slug_name'] != slugNameMovie:
            peliculas.append(movie)
    
    nuevaCesta['cesta'] = peliculas
    
    with open('app/usuarios/' + username + '/cesta.json', 'w') as file:
            json.dump(nuevaCesta, file, indent=4)
    
    return redirect(url_for('cesta'))

@app.route('/cuenta', methods=['GET', 'POST'])
def cuenta():
    username = getUsernameActual()
    
    if username != "Anonymous":
        if os.path.exists("app/usuarios/" + username) == True:
            # Lee los datos del usuario
            datos = leerUser(username)
            
            # Si se quiere aniaidr dinero se modifican los datos del usuario
            if 'newbudget' in request.form:
                datos['budget'] = str(float(datos['budget']) + float(request.form['newbudget']))
                escribirUser(username, datos)
            
            # Se intenta leer el historial de compras del usuario
            catalogue = leerCatalogue('usuarios/' + username + '/historial.json', 'historial')
            return render_template('cuenta.html', title="Cuenta", datos=datos, movies=catalogue['historial'])
        else:
            return render_template('register.html', title="Sign Up")
    else:
        return render_template('login.html', title='Sign In')
