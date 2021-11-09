import sys
import traceback
import random
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

        query = "SELECT MV.movietitle AS title, MV.movieid AS id"
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
            query += " lower(title) like '%%" + str(lower_name_filter) + "%%'"

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
        movies = list(db_conn.execute(
            "SELECT MV.movietitle AS title, MV.movieid, " \
            "MV.year AS date, DR.directorname AS director, " \
            "ML.language AS language, MG.genre AS genre, PD.price AS price " \
            "FROM imdb_movies AS MV " \
            "NATURAL JOIN imdb_directormovies " \
            "NATURAL JOIN imdb_directors AS DR " \
            "NATURAL JOIN imdb_movielanguages AS ML " \
            "NATURAL JOIN imdb_moviegenres AS MG " \
            "NATURAL JOIN products AS PD " \
            "WHERE MV.movieid = " + str(movieid) + \
            " LIMIT 1"))
        db_conn.close()
        if len(movies) == 0:
            return None
        else:
            return movies[0]
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
                creditcard,
                country,
                city,
                addres):
    try:
        # Conecta con la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Crea el id del cliente
        customer_id = list(db_conn.execute("SELECT COUNT(customerid) "
                                           "as c FROM customers"))
        customer_id = int(customer_id[0].c) + 1

        # Se crean datos para simplificar la funcion register
        expiration = datetime.today() + timedelta(weeks=10)
        expiration = expiration.strftime('%Y-%m-%d')

        db_conn.execute(
            "INSERT INTO customers (customerid, firstname, lastname, " \
            "address1, city, country, creditcardtype, creditcard, " \
            "creditcardexpiration, username, password) " \
            "VALUES (" + str(customer_id) + ", " + str(firstname) + ", " + \
            str(lastname) + ", " + str(addres) + ", " + str(city) + ", " + \
            str(country) + ", credit, " + str(creditcard) + ", " + \
            str(expiration) + ", " + str(username) + ", " + \
            str(password) + ")")

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
                            "(" + str(order_id) + ", " + str(user_id) + \
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
            "SELECT CM.username, OD.status, OD.totalamount, OT.prod_id, " \
            "OT.price AS price, OT.quantity AS quantity, MV.movieid AS id, " \
            " MV.movietitle AS title " \
            "FROM customers AS CM NATURAL JOIN " \
            "orders AS OD NATURAL JOIN " \
            "ordertail AS OT NATURAL JOIN " \
            "products NATURAL JOIN " \
            "imdb_movies AS MV " \
            "WHERE CM.username = '" + username + "' " \
            "AND OD.status = 'ON' " \
            "GROUP BY OT.prod_id"))

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
        info = list(db_conn.execute(
            "SELECT CM.username, CM.income, OR.orderid, OR.totalamount, " \
            "OR.status " \
            "FROM customers AS CM NATURAL JOIN orders AS OR " \
            "WHERE CM.username = '" + usesrname + "' " \
            "AND OR.status = 'ON'"))

        # Si el carrito esta vacio lo indica
        if len(info) == 0:
            return "Carrito vacio"

        info = info[0]

        # Calcula el saldo restante
        left = info["CM.income"] - info["OR.totalamount"]
        # Si el saldo es insuficiente lo indica
        if left < 0:
            return "Saldo insuficiente"

        # Actualiza el saldo del usuario
        db_conn.execute(
            "UPDATE customers " \
            "SET income = " + str(left) + \
            " WHERE username = '" + str(username) + "'")

        # Actualiza el estado del pedido a acabado
        db_conn.execute(
            "UPDATE orders " \
            "SET status = 'ENDED' " \
            "WHERE orderid = " + str(info["OR.orderid"]))

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
def add_to_cart(username, movieId, quantity):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene el producto
        prod_id = list(db_conn.execute("SELECT prod_id, movieid, price " \
                                       "FROM products " \
                                       "WHERE movieid = " + str(movieId)))
        if len(prod_id) < 1:
            return None

        # Averigua el precio y el id
        price = prod_id[0]["price"]
        prod_id = prod_id[0]["prod_id"]

        # Averigua el id del cliente
        user_id = list(db_conn.execute("SELECT * FROM customers "
                                       "WHERE username='" + username + "'"))
        user_id = user_id[0]["customerid"]

        # Crea u obtiene un carrito abierto
        db_conn.close()
        order_id = get_or_create_cart(user_id)
        db_conn = db_engine.connect()

        db_conn.execute("INSERT INTO ordertail (orderid, prod_id, price, " \
                        "quantity) VALUES (" + str(order_id) + ", " + \
                        str(prod_id) + ", " + str(price) + ", " + \
                        str(quantity) + ")")

        # Actualiza el precio del carrito
        aux = list(db_conn.execute(
            "SELECT orderid, netamount, tax, totalamount " \
            "FROM orders " \
            "WHERE orderid = " + order_id))
        net = aux[0]["netamount"]
        tax = aux[0]["tax"]
        total = aux[0]["totalamount"]

        net = net + int(quantity) * price
        total = net * tax + net

        db_conn.execute(
            "UPDATE orders " \
            "SET netamount = " + str(net) + ", totalamount = " + set(total) + \
            " WHERE ordersid = " + str(order_id))

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
def mod_ordertail(username, movieid, quantity):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Encuentra y obtiene informacion del pedido
        info = list(db_conn.execute(
            "SELECT CM.username, OR.orderid, OR.status, OR.netamount, " \
            "OR.tax, OT.prod_id, OT.price, OT.quantity, PD.movieid " \
            "FROM customers AS CM NATURAL JOIN orders AS OR NATURAL JOIN " \
            "ordertail AS OT NATURAL JOIN products AS PD " \
            "WHERE CM.username = '" + username + "' " \
            "AND OR.status = 'ON' " \
            "AND PD.movieid = " + str(movieid)))
        info = info[0]

        # Recalcula el nuevo precio
        netamount = info["OR.netamount"]
        netamount -= info["OT.price"] * info["OT.quantity"]
        netamount += info["OT.price"] * quantity
        totalamount = netamount + netamount * info["tax"]

        # Actualiza el precio del pedido
        db_conn.execute(
            "UPDATE orders " \
            "SET netamount = " + str(netamount) + ", " \
            "totalamount = " + str(totalamount) + \
            " WHERE orderid = " + str(info["OR.orderid"]))

        # Si la cantidad es 0 elimina el producto
        if quantity == 0:
            db_conn.execute(
                "DELETE FROM ordertail " \
                "WHERE orderid = " + str(info["OR.orderid"]) + \
                " AND prod_id = " + str(info["OT.prod_id"]))
        # Actualiza la cantidad
        else:
            db_conn.execute(
                "UPDATE ordertail " \
                "SET quantity = " + str(quantity) + \
                " WHERE orderid = " + str(info["OR.orderid"]) + \
                " AND prod_id = " + str(info["OT.prod_id"]))

        db_conn.close()
        return
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)
    return None


# Devuelve el historial de pedidos
def get_historial(usesrname):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene el historial
        info = list(db_conn.execute(
            "SELECT CM.username, OR.orderid, OR.orderdate, " \
            "OR.totalamount, OR.status, OT.price, OT.quantity, " \
            "MV.movieid, MV.movietitle " \
            "FROM customers AS CM NATURAL JOIN orders AS OR " \
            "NATURAL JOIN ordertail AS OT NATURAL JOIN products " \
            "NATURAL JOIN imdb_movies AS MV " \
            "WHERE CM.username = '" + username + \
            " AND OR.status = 'ENDED'"))

        # Agrupa el historial por pedidos
        historial = {}
        for i in info:
            id = i["OR.orderid"]
            if id not in historial:
                historial[id] = {"date": i["OR.orderdate"],
                                 "price": i["OR.totalamount"],
                                 "movies": []}
            historial[id]["movies"].append({"title": i["MV.movietitle"],
                                            "id": i["MV.movieid"],
                                            "quantity": i["OT.quantity"],
                                            "price": i["OT.price"]})

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
