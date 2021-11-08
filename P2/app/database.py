import sys
import traceback
import datetime
from sqlalchemy import MetaData
from sqlalchemy import create_engine

######## DataBasa ########

# Configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:"
                          "alumnodb@localhost/si1",
                          echo=False)
db_meta = MetaData(bind=db_engine)


######## Funciones generales ########

#### MOVIES ####

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
def list_movies(name_filter=None, genre_filter=None):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Crea el SELECT
        query = "SELECT MV.movietitle, MV.movieid"
        if genre_filter != None:
            query += ", GR.movieid, GR.genre"

        # Crea el FROM
        query += " FROM imdb_movies AS MV"
        if genre_filter != None:
            query += ", imdb_moviegenres AD GR"

        # Crea el WHERE
        if genre_filter != None:
            query += " WHERE MV.movieid = GR.movieid \
                      AND GR.genre = '" + str(genre_filter) + "' "
        if name_filter != None:
            if genre_filter == None:
                query += " WHERE"
            else:
                query += " AND"
            lower_name_filter = name_filter.lower()
            query += " lower(MV.movietitle) like '%%" + str(lower_name_filter) + "%%' "

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
def get_movie(movieid):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        movies = list(db_conn.execute("SELECT * "
                                      "FROM imdb_movies "
                                      "WHERE movieid = '" + str(movieid) + "'"))
        db_conn.close()
        if len(movies) == 1:
            return movies[0]
        else:
            return None
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


## AUTHENTICATIONS ##

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


######################################## COMPLETAR ########################################
def create_user(username):
    try:
        # Conecta con la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Crea el id del cliente
        customer_id = list(db_conn.execute("SELECT COUNT(customerid) "
                                           "as c FROM customers"))
        customer_id = int(customer_id[0].c) + 1

        # Crea el id de la tarheta de credito
        creditcard_id = list(db_conn.execute("SELECT COUNT(creditcard_id)"
                                             " as c FROM creditcards"))
        creditcard_id = int(creditcard_id[0].c) + 1

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

	return 'ERR'


## CARRITO ##

# Crea un carrito
def get_or_create_cart(user_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Comprueba si hay algun carrito sin finalizar
        orders = list(db_conn.execute("SELECT orderid, status " \
                                      "FROM orders " \
                                      "WHERE customerid = " + str(user_id) + \
                                      " AND status = 'ON'")
        # Si no hay ningun carrito abierto lo crea
        if len(orders) == 0:
            order_id = list(db_conn.execute("SELECT COUNT(orderid) as c 
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
                        str(quantity))

        # Actualiza el precio del carrito
        aux = list(db_conn.execute(
            "SELECT orderid, netamount, tax, totalamount " \
            "FROM orders " \
            "WHERE orderid = " + order_id))
        net = aux[0]["netamount"]
        tax = aux[0]["tax"]
        total = aux[0]["totalamount"]

        net = net + quantity * price
        total = net * tax + net

        db_conn.execute(
            "UPDATE orders " \
            "SET netamount = " str(net) + ", totalamount = " + set(total) \
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










































