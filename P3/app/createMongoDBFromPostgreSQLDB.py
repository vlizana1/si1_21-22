import os
import sys, traceback
import psycopg2
import difflib
import sqlalchemy as SQL
import pymongo as pyMNG

# Motor de sqlalchemy
db_engine = SQL.create_engine("postgresql://alumnodb:alumnodb@localhost/si1",
                              echo=False)


# Conecta con la base de datos
try:
    db_conn = db_engine.connect()
except Exception:
    print("ERROR conecting database")
    exit()


# Datos de busqueda
numPelis = 400
pais = "UK"


# Querys
query_topMovies = "SELECT MV.movieid AS movieid, MV.movietitle AS movietitle, " \
                         "MV.year AS year, MC.country " \
                  "FROM imdb_movies AS MV NATURAL JOIN " \
                       "imdb_moviecountries AS MC " \
                  "WHERE MC.country = '%%PAIS%%' " \
                  "ORDER BY MV.year DESC " \
                  "LIMIT %%NUM%%;"

query_movieGenres = "SELECT * " \
                    "FROM imdb_moviegenres " \
                    "WHERE movieid = %%ID%%;"

query_movieDirectors = "SELECT DM.movieid, DR.directorname AS directorname " \
                       "FROM imdb_directormovies AS DM NATURAL JOIN " \
                            "imdb_directors AS DR " \
                       "WHERE DM.movieid = %%ID%%;"

query_movieActors = "SELECT AC.actorname AS actorname, AM.movieid " \
                    "FROM imdb_actors AS AC NATURAL JOIN " \
                         "imdb_actormovies AS AM " \
                    "WHERE AM.movieid = %%ID%%;"


# Obtiene las peliculas
movies = []
for movie in list(db_conn.execute(query_topMovies.replace("%%PAIS%%", pais).replace("%%NUM%%", str(numPelis)))):
    if movie:
        # Titulo sin la fecha
        title = movie["movietitle"].split(" (")
        title = title[0]

        # Anio
        year = int(movie["year"])

        # Generos
        genres = []
        for genre in db_conn.execute(query_movieGenres.replace("%%ID%%", str(movie["movieid"]))):
            if genre and genre not in genres:
                genres.append(genre["genre"])

        # Directores
        directors = []
        for director in db_conn.execute(query_movieDirectors.replace("%%ID%%", str(movie["movieid"]))):
            if director and director not in directors:
                directors.append(director["directorname"])

        # Actores
        actors = []
        for actor in db_conn.execute(query_movieActors.replace("%%ID%%", str(movie["movieid"]))):
            if actor[0] != "" and actor not in actors:
                actors.append(actor["actorname"])

        # Aniade la pelicula y su informacion a la lista
        movies.append({"title"              : title,
                       "genres"             : genres,
                       "year"               : year,
                       "directors"          : directors,
                       "actors"             : actors,
                       "most_related_movies": [],
                       "related_movies"     : []})


# Peliculas relacionadas y mas relacionadas
for i in range(len(movies)):
    m1 = movies[i]
    if len(m1["genres"]) > 0:
        for m2 in movies[i:]:
            if len(m2["genres"]) > 0:
                # Coincidencia de generos
                c = (len(set(m1["genres"]) & set(m2["genres"])) / len(set(m1["genres"]) | set(m2["genres"]))) * 100

                if c == 100 and len(m1["genres"]) > 1 and len(m2["genres"]):
                    if len(m1["most_related_movies"]) < 10:
                        m1["most_related_movies"].append({"title": m2["title"],
                                                          "year": m2["year"]})
                    if len(m2["most_related_movies"]) < 10:
                        m2["most_related_movies"].append({"title": m1["title"],
                                                          "year": m1["year"]})
                elif c >= 50:
                    if len(m1["related_movies"]) < 10:
                        m1["related_movies"].append({"title": m2["title"],
                                                     "year": m2["year"]})
                    if len(m2["related_movies"]) < 10:
                        m2["related_movies"].append({"title": m1["title"],
                                                     "year": m1["year"]})


# Cierra la conexion con la base de datos
db_conn.close()

# Conecta con mongoDB
mngClient = pyMNG.MongoClient("mongodb://localhost:27017/")

# Obtiene la DB
db = mngClient["si1"]

# Borra y aniade el topUSA
coleccion = db["topUK"]
coleccion.drop()
coleccion = db["topUK"]
coleccion.insert_many(movies)
