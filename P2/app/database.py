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

        query = "SELECT MV.movieid, MV.movietitle, GR.movieid, GR.genre \
                 FROM imdb_movies AS MV, imdb_moviegenres AD GR \
                 WHERE MV.movieid = GR.movieid "
        if name_filter != None:
            query += "AND lower(MV.movietitle) like '%%" + str(name_filter) + "%%' "
        if genre_filter != None:
            query += "AND GR.genre = '" + str(genre_filter) + "' "
        query += "ORDER BY MV.movietitle"

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


# Devuelve una lista de todos lo generos
def list_genres():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        genres = list(db_conn.execute("SELECT genre "
                                      "FROM imdb_moviegenres "
                                      "GROUP BY genre "
                                      "ORDER BY genre"))
        db_conn.close()
        return genres
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)


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













































