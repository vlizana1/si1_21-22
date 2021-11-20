import sys
import traceback
import random
from decimal import *
from datetime import datetime, timedelta
from sqlalchemy import MetaData
from sqlalchemy import create_engine


# Configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:"
                          "alumnodb@localhost/si1",
                          echo=False)
db_meta = MetaData(bind=db_engine)


######## MOVIES ########

# Devuelve toda la informacion sobre todas las peliculas
def all_movies_info():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        all_movies_info = list(db_conn.execute("SELECT * FROM imdb_movies "
                                               "ORDER BY movietitle"))
        db_conn.close()
        return all_movies_info
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return None


# Devuelve una lista de todas las peliculas
def list_movies(name_filter=None, genre_filter=None, lim=None):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        query = "SELECT MV.movietitle AS title, MV.year AS date, " \
                "MV.movieid AS id"
        if genre_filter != None:
            query += ", GR.genre"

        query += " FROM imdb_movies AS MV"
        if genre_filter != None:
            query += " NATURAL JOIN imdb_moviegenres AS GR" \
                     " WHERE GR.genre = '" + str(genre_filter) + "'"

        if name_filter != None:
            lower_name_filter = name_filter.lower()
            if genre_filter == None:
                query += " WHERE"
            else:
                query += " AND"
            query += " lower(MV.movietitle) like '%%" + str(lower_name_filter) + "%%'"

        if lim != None:
            query += " LIMIT " + str(lim)

        list_all_movies = list(db_conn.execute(query))
        db_conn.close()

        return list_all_movies
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return None


# Devuelve una pelicula
def get_movie_info(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        movie = list(db_conn.execute(
            "SELECT MV.movieid, MV.movietitle AS title, " \
            "MV.year AS date " \
            "FROM imdb_movies AS MV " \
            "WHERE MV.movieid = " + str(movieid) + \
            " LIMIT 1"))
        if len(movie) == 0:
            info = {"title": None}
            print("NO EMNCONTRADO")
        else:
            info = {"title": movie[0]["title"],
                    "date": movie[0]["date"],
                    "genres": get_movie_genres(movieid),
                    "languages": get_movie_languages(movieid),
                    "countries": get_movie_countries(movieid),
                    "directors": get_movie_director(movieid),
                    "actors": get_movie_actors(movieid),
                    "products": get_movie_products(movieid)}
        db_conn.close()
        return info
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def get_movie_genres(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        genres = list(db_conn.execute(
            "SELECT movieid, genre " \
            "FROM imdb_moviegenres " \
            "WHERE movieid = " + str(movieid)))
        db_conn.close()
        return genres
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def get_movie_languages(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        languages = list(db_conn.execute(
            "SELECT movieid, language " \
            "FROM imdb_movielanguages " \
            "WHERE movieid = " + str(movieid)))
        db_conn.close()
        return languages
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def get_movie_countries(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        countries = list(db_conn.execute(
            "SELECT movieid, country " \
            "FROM imdb_moviecountries " \
            "WHERE movieid = " + str(movieid)))
        db_conn.close()
        return countries
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def get_movie_director(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        director = list(db_conn.execute(
            "SELECT DM.movieid, DR.directorname AS director " \
            "FROM imdb_directormovies AS DM NATURAL JOIN " \
            "imdb_directors AS DR "
            "WHERE DM.movieid = " + str(movieid)))
        db_conn.close()
        return director[0]
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def get_movie_actors(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        actors = list(db_conn.execute(
            "SELECT AM.movieid, AM.\"character\" AS character, " \
            "AM.creditsposition AS cp, AC.actorname AS name, " \
            "AC.gender AS gender " \
            "FROM imdb_actormovies AS AM NATURAL JOIN " \
            "imdb_actors AS AC " \
            "WHERE AM.movieid = " + str(movieid) + \
            " ORDER BY AC.actorname"))
        db_conn.close()
        return actors
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def get_movie_products(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        products = list(db_conn.execute(
            "SELECT PD.movieid, PD.prod_id AS id , PD.price AS price, " \
            "PD.description AS description, INV.stock AS stock, " \
            "INV.sales AS sales " \
            "FROM products AS PD NATURAL JOIN inventory AS INV " \
            "WHERE PD.movieid = " + str(movieid) + \
            " AND INV.stock > 0 " \
            "ORDER BY PD.price"))
        db_conn.close()
        return products
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Devuelve una lista de todos lo generos
def list_genres():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        genres = list(db_conn.execute("SELECT genre "
                                      "FROM imdb_moviegenres "
                                      "GROUP BY genre"))
        db_conn.close()
        return genres
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


######## AUTHENTICATIONS ########

# Devuelve informacion para un usuario con su contrasenia
def get_user(username, password):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        list_costum = list(db_conn.execute("SELECT * FROM customers "
                                           "WHERE username='" + username + "' "
                                           "and password='" + password + "'"))
        db_conn.close()
        return list_costum
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

    return None


def get_user_minor_info(username):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        user = list(db_conn.execute(
            "SELECT username, firstname, lastname, email, income " \
            "FROM customers " \
            "WHERE username = '" + username + "'"))

        db_conn.close()
        return user[0]
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def create_user(username,
                password, 
                firstname,
                lastname,
                email,
                creditcard):
    try:
        # Conecta con la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Crea el id del cliente
        customer_id = list(db_conn.execute("SELECT COUNT(customerid) "
                                           "as c FROM customers"))
        customer_id = int(customer_id[0].c) + 1

        income = random.randint(0, 200)

        # Se crean datos para simplificar la funcion register
        expiration = datetime.today() + timedelta(weeks=10)
        expiration = expiration.strftime('%Y-%m-%d')

        db_conn.execute(
            "INSERT INTO customers (customerid, firstname, lastname, " \
            "email, creditcardtype, creditcard, creditcardexpiration, " \
            "income, username, password) " \
            "VALUES (" + str(customer_id) + ", '" + str(firstname) + \
            "', '" + str(lastname) + "', '" + str(email) + \
            "', 'credit', '" + str(creditcard) + "', '" + \
            str(expiration) + "', " +str(income) + ", '" + str(username) + \
            "', '" + str(password) + "')")

        return customer_id
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Indica si existe un username
def username_exists(username):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        result = list(db_conn.execute("SELECT count(customerid) "
                                      "as c FROM customers "
                                      "WHERE username = '" + username + "'"))
        db_conn.close()
        if len(result) > 0 and int(result[0].c) != 0:
            return True
        else:
            return False
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Indica si existe un email
def email_exists(email):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        result = list(db_conn.execute("SELECT count(email) "
                                      "as c FROM customers "
                                      "WHERE email = '" + email + "'"))
        db_conn.close()
        if len(result) > 0 and int(result[0].c) != 0:
            return True
        else:
            return False

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


######## CARRITO ########

# Crea un carrito
def get_or_create_cart(user_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Comprueba si hay algun carrito sin finalizar
        orders = list(db_conn.execute("SELECT orderid, status " \
                                      "FROM orders " \
                                      "WHERE customerid = " + str(user_id) + \
                                      " AND status = 'ON'"))
        # Si no hay ningun carrito abierto lo crea
        if len(orders) == 0:
            order_id = list(db_conn.execute("SELECT COUNT(orderid) as c " \
                                            "FROM orders"))
            order_id = int(order_id[0].c) + 1
            db_conn.execute("INSERT INTO orders (orderid, customerid, " \
                            "orderdate, netamount, totalamount, status) VALUES " \
                            "('" + str(order_id) + "', " + str(user_id) + \
                            ", now(), 0, 0, 'ON')")
        else:
            order_id = orders[0]["orderid"]

        db_conn.close()
        return order_id
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Devuelve al carrito abierto
def get_actual_cart(username):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        cart = list(db_conn.execute(
            "SELECT CM.username, OD.status, OD.totalamount AS amount, " \
            "OT.prod_id AS prod_id, OT.price AS price, " \
            "OT.quantity AS quantity, MV.movieid AS id, " \
            "MV.movietitle AS title, INV.stock AS stock, " \
            "PD.description AS description " \
            "FROM customers AS CM NATURAL JOIN " \
            "orders AS OD NATURAL JOIN " \
            "orderdetail AS OT NATURAL JOIN " \
            "products AS PD NATURAL JOIN " \
            "inventory AS INV NATURAL JOIN " \
            "imdb_movies AS MV " \
            "WHERE CM.username = '" + username + "' " \
            "AND OD.status = 'ON'" \
            "ORDER BY OD.orderdate DESC"))

        for p in cart:
            if int(p["stock"]) < int(p["quantity"]):
                p["ERR"] = "Stock insuficiente, quedan " + \
                           str(p["stock"]) + " unidades disponibles"

        db_conn.close()
        return cart
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Termina la compra del carrito
def end_cart(username):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene informacion sobre el usuario y el pedido
        prods = list(db_conn.execute(
            "SELECT CM.username, CM.income AS income, ORD.status, " \
            "ORD.totalamount AS totalamount, ORD.orderid AS oid, " \
            "OT.quantity AS quantity, OT.prod_id AS id, INV.stock AS stock " \
            "FROM customers AS CM NATURAL JOIN orders AS ORD " \
            "NATURAL JOIN orderdetail AS OT NATURAL JOIN products " \
            "NATURAL JOIN inventory AS INV " \
            "WHERE CM.username = '" + str(username) + "' " \
            "AND ORD.status = 'ON'"))

        # Si el carrito esta vacio lo indica
        if len(prods) == 0:
            db_conn.close()
            return "Carrito vacio"

        
        # Calcula el saldo restante
        left = Decimal(prods[0]["income"]) - Decimal(prods[0]["totalamount"])
        # Si el saldo es insuficiente lo indica
        if left < 0:
            db_conn.close()
            return "Saldo insuficiente"

        for p in prods:
            if int(p["stock"]) < int(p["quantity"]):
                db_conn.close()
                return "Revisa los items"

        # Actualiza el stock de las peliculas
        for p in prods:
            db_conn.execute(
                "UPDATE inventory " \
                "SET stock = " + str(int(p["stock"]) - int(p["quantity"])) + \
                "WHERE prod_id = " + str(p["id"]))

        # Actualiza el saldo del usuario
        db_conn.execute(
            "UPDATE customers " \
            "SET income = " + str(left) + \
            " WHERE username = '" + str(username) + "'")

        # Actualiza el estado del pedido a acabado
        db_conn.execute(
            "UPDATE orders " \
            "SET status = 'ENDED' " \
            "WHERE orderid = " + str(prods[0]["oid"]))

        db_conn.close()
        return None
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Aniade una pelicula al carrito
def add_to_cart(username, prod_id, quantity):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene el producto
        info = list(db_conn.execute("SELECT prod_id, price " \
                                    "FROM products " \
                                    "WHERE prod_id = " + str(prod_id)))
        if len(info) < 1:
            return None

        # Averigua el precio y el id
        price = info[0]["price"]

        # Averigua el id del cliente
        user_id = list(db_conn.execute("SELECT * FROM customers "
                                       "WHERE username = '" + str(username) + "'"))
        user_id = user_id[0]["customerid"]

        # Crea u obtiene un carrito abierto
        db_conn.close()
        order_id = get_or_create_cart(user_id)
        db_conn = db_engine.connect()

        exist = list(db_conn.execute(
            "SELECT orderid, prod_id, quantity " \
            "FROM orderdetail " \
            "WHERE orderid = " + str(order_id) + \
            " AND prod_id = " + str(prod_id)))

        if len(exist) > 0:
            newQ = Decimal(exist[0]["quantity"]) + Decimal(quantity)
            mod_orderdetail(username, prod_id, newQ)
            return None

        db_conn.execute("INSERT INTO orderdetail (orderid, prod_id, price, " \
                        "quantity) VALUES (" + str(order_id) + ", " + \
                        str(prod_id) + ", " + str(price) + ", " + \
                        str(quantity) + ")")

        # Actualiza el precio del carrito
        aux = list(db_conn.execute(
            "SELECT orderid, netamount, tax, totalamount " \
            "FROM orders " \
            "WHERE orderid = " + str(order_id)))
        net = aux[0]["netamount"]
        tax = aux[0]["tax"]
        total = aux[0]["totalamount"]

        net = net + int(quantity) * price
        #total = net * tax + net
        total = net * Decimal(0.21) + net

        db_conn.execute(
            "UPDATE orders " \
            "SET netamount = " + str(net) + \
            ", totalamount = " + str(total) + \
            " WHERE orderid = " + str(order_id))

        db_conn.close()
        return order_id
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Modifica o elimina un producto de un pedido
def mod_orderdetail(username, prodid, quantity):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Encuentra y obtiene informacion del pedido
        info = list(db_conn.execute(
            "SELECT CM.username, ORD.orderid AS id, ORD.status, " \
            "ORD.netamount AS amount, ORD.tax AS TAX, OT.prod_id, " \
            "OT.price AS price, OT.quantity AS quantity, PD.movieid " \
            "FROM customers AS CM NATURAL JOIN orders AS ORD NATURAL JOIN " \
            "orderdetail AS OT NATURAL JOIN products AS PD " \
            "WHERE CM.username = '" + str(username) + "' " \
            "AND ORD.status = 'ON' " \
            "AND PD.prod_id = " + str(prodid)))
        info = info[0]

        # Recalcula el nuevo precio
        netamount = Decimal(info["amount"])
        netamount -= Decimal(info["price"]) * Decimal(info["quantity"])
        netamount += Decimal(info["price"]) * Decimal(quantity)
        #totalamount = Decimal(netamount) + Decimal(netamount) * Decimal(info["tax"])
        totalamount = Decimal(netamount) + Decimal(netamount) * Decimal(0.21)

        # Actualiza el precio del pedido
        db_conn.execute(
            "UPDATE orders " \
            "SET netamount = " + str(netamount) + ", " \
            "totalamount = " + str(totalamount) + \
            " WHERE orderid = " + str(info["id"]))

        # Si la cantidad es 0 elimina el producto
        if int(quantity) == 0:
            db_conn.execute(
                "DELETE FROM orderdetail " \
                "WHERE orderid = " + str(info["id"]) + \
                " AND prod_id = " + str(prodid))
        # Actualiza la cantidad
        else:
            db_conn.execute(
                "UPDATE orderdetail " \
                "SET quantity = " + str(quantity) + \
                " WHERE orderid = " + str(info["id"]) + \
                " AND prod_id = " + str(prodid))

        db_conn.close()
        return None
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Devuelve el historial de pedidos
def get_historial(username):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene el historial
        info = list(db_conn.execute(
            "SELECT CM.username, ORD.orderid AS id, ORD.orderdate AS date, " \
            "ORD.totalamount AS amount, ORD.status, OT.price AS price, " \
            "OT.quantity AS quantity, MV.movieid AS mid, " \
            "MV.movietitle AS title, PD.description AS description " \
            "FROM customers AS CM NATURAL JOIN orders AS ORD " \
            "NATURAL JOIN orderdetail AS OT NATURAL JOIN products AS PD " \
            "NATURAL JOIN imdb_movies AS MV " \
            "WHERE CM.username = '" + username + "'" + \
            " AND ORD.status = 'ENDED' " \
            "ORDER BY ORD.orderdate DESC"))

        # Agrupa el historial por pedidos
        aux = {}
        for i in info:
            id = i["id"]
            if id not in aux:
                aux[id] = {"date": i["date"],
                           "price": i["amount"],
                           "movies": []}
            aux[id]["movies"].append({"title": i["title"],
                                      "id": i["mid"],
                                      "description": i["description"],
                                      "quantity": i["quantity"],
                                      "price": i["price"]})

        # Transforma historial en algo legible por el html
        historial = []
        for id in aux.keys():
            historial.append({"id": id,
                              "date": aux[id]["date"],
                              "price": aux[id]["price"],
                              "movies": aux[id]["movies"]})

        db_conn.close()
        if len(historial) == 0:
            return None
        return historial
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


def add_budget(username, addedBudget):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        income = list(db_conn.execute(
            "SELECT username, income " \
            "FROM customers " \
            "WHERE username = '" + str(username) + "'"))

        income = income[0]["income"]
        income = int(income) + int(addedBudget)

        db_conn.execute(
            "UPDATE customers " \
            "SET income = " + str(income) + \
            " WHERE username = '" + str(username) + "'")

        db_conn.close()
        return historial
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None
