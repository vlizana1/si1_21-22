# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine
from pymongo import MongoClient

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

# Crea la conexión con MongoDB
mongo_client = MongoClient()

def getMongoCollection(mongoDB_client):
    mongo_db = mongoDB_client.si1
    return mongo_db.topUK


def mongoDBCloseConnect(mongoDB_client):
    mongoDB_client.close();


def dbConnect():
    return db_engine.connect()


def dbCloseConnect(db_conn):
    db_conn.close()


def findTop(title=None, genre=None, year=None, actor=None):
    params = {"$and": []}

    if title:
        params["$and"].append({"title": {"$regex": str(title), "$options": "i"}})

    if genre:
        if isinstance(genre, list):
            for g in genre:
                params["$and"].append({"genres": {"$regex" : str(g), "$options" : "i"}})
        else:
            params["$and"].append({"genres": {"$regex" : str(genre), "$options" : "i"}})

    if year:
        if isinstance(year, list):
            params["$and"].append({"year": {"$in": year}})
        else:
            params["$and"].append({"year": {"$eq": year}})

    if actor:
        if isinstance(actor, list):
            for a in actor:
                params["$and"].append({"actors": {"$regex" : str(a), "$options" : "i"}})
        else:
            params["actors"] = {"$regex" : str(actor), "$options" : "i"}

    movies = getMongoCollection(mongo_client)
    return list(movies.find(params))


def delCity(city, bFallo, bSQL, duerme, bCommit):
    # Array de trazas a mostrar en la página
    dbr=[]

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()

    # Customers
    query_get_customers = "SELECT customerid " \
                          "FROM customers " \
                          "WHERE city = '" + str(city) + "'"
    query_count_customers = "SELECT COUNT(*) " \
                            "FROM customers " \
                            "WHERE city = '" + str(city) + "'"
    query_delete_customers = "DELETE FROM customers " \
                             "WHERE city = '" + str(city) + "'"

    # Orders
    query_get_orders = "SELECT orderid " \
                       "FROM orders " \
                       "WHERE customerid IN (" + query_get_customers + ")"
    query_count_orders = "SELECT COUNT(*) " \
                         "FROM orders " \
                         "WHERE customerid IN (" + query_get_customers + ")"
    query_delete_orders = "DELETE FROM orders " \
                          "WHERE customerid IN (" + query_get_customers + ")"

    # Orderdetail
    query_get_orderdetail = "SELECT orderid " \
                            "FROM orderdetail " \
                            "WHERE orderid IN (" + query_get_orders + ")"
    query_count_orderdetail = "SELECT COUNT(*) " \
                              "FROM orderdetail " \
                              "WHERE orderid IN (" + query_get_orders + ")"
    query_delete_orderdetail = "DELETE FROM orderdetail " \
                               "WHERE orderid IN (" + query_get_orders + ")"
    
    db_conn = dbConnect()
    try:
        # TODO: ejecutar consultas
        # Se ejecuta para que falle
        if bFallo:
            dbr.append("Ejecutando transaccion en orden erroneo (ordertail, customers, orders")
            res = db_conn.execute("BEGIN;")
            dbr.append("  >  BEGIN")
            
            # Ordertail
            res = db_conn.execute(query_delete_orderdetail).rowcount
            dbr.append("> DELETE FROM orderdetail ...")
            dbr.append(">>> " + str(res) + " filas eliminadas en 'orderdetail'")

            res = db_conn.execute(query_count_orderdetail).fetchone()
            dbr.append("> SELECT COUNT(*) FROM orderdetail ...")
            dbr.append(">>> Ahora hay '" + str(res[0]) + "' filas en 'orderdetail'")
            
            # Commit
            if bCommit is True:
                dbr.append("  Realizamos el COMMIT")
                res = db_conn.execute("COMMIT;")
                dbr.append("  >  COMMIT")
                res = db_conn.execute("BEGIN;")
                dbr.append("  >  BEGIN")

            # Customers
            res = db_conn.execute(query_delete_customers).rowcount
            dbr.append("> DELETE FROM customers ...")
            dbr.append(">>> " + str(res) + " filas eliminadas en 'customers'")
            if duerme:
                time.sleep(float(duerme))

            res = db_conn.execute(query_count_customers).fetchone()
            dbr.append("> SELECT COUNT(*) FROM customers ...")
            dbr.append(">>> Ahora hay '" + str(res[0]) + "' filas en 'customers'")

            # Orders
            res = db_conn.execute(query_delete_orders).rowcount
            dbr.append("> DELETE FROM orders ...")
            dbr.append(">>> " + str(res) + " filas eliminadas en 'orders'")

            res = db_conn.execute(query_count_orders).fetchone()
            dbr.append("> SELECT COUNT(*) FROM orders ...")
            dbr.append(">>> Ahora hay '" + str(res[0]) + "' filas en 'orders'")

            res = db_conn.execute("COMMIT;")
            dbr.append("> COMMIT")

        # Se ejecuta correctamente
        else:
            dbr.append("Ejecutando transaccion en orden correcto (ordertail, orders, customers)")
            res = db_conn.execute("BEGIN;")
            dbr.append("> BEGIN")

            # Ordertail
            res = db_conn.execute(query_delete_orderdetail).rowcount
            dbr.append("> DELETE FROM orderdetail ...")
            dbr.append(">>> " + str(res) + " filas eliminadas en 'orderdetail'")

            res = db_conn.execute(query_count_orderdetail).fetchone()
            dbr.append("> SELECT COUNT(*) FROM orderdetail ...")
            dbr.append(">>> Ahora hay '" + str(res[0]) + "' filas en 'orderdetail'")
            
            # Commit
            if bCommit is True:
                dbr.append(">>> Realizamos el COMMIT")
                res = db_conn.execute("COMMIT;")
                dbr.append("> COMMIT")
                res = db_conn.execute("BEGIN;")
                dbr.append("> BEGIN")

            # Orders
            res = db_conn.execute(query_delete_orders).rowcount
            dbr.append("> DELETE FROM orders ...")
            dbr.append(">>> " + str(res) + " filas eliminadas en 'orders'")

            res = db_conn.execute(query_count_orders).fetchone()
            dbr.append("> SELECT COUNT(*) FROM orders ...")
            dbr.append(">>> Ahora hay '" + str(res[0]) + "' filas en 'orders'")

            # Customers
            res = db_conn.execute(query_delete_customers).rowcount
            dbr.append("> DELETE FROM customers ...")
            dbr.append(">>> " + str(res) + " filas eliminadas en 'customers'")
            if duerme:
                time.sleep(float(duerme))

            res = db_conn.execute(query_count_customers).fetchone()
            dbr.append("> SELECT COUNT(*) FROM customers ...")
            dbr.append(">>> Ahora hay '" + str(res[0]) + "' filas en 'customers'")

            res = db_conn.execute("COMMIT;")
            dbr.append("> COMMIT")
    except Exception as e:
        print(e)
        # TODO: deshacer en caso de error
        dbr.append("Se ha producido algun error")
        res = db_conn.execute("ROLLBACK;")
        dbr.append("> ROLLBACK")

        res = db_conn.execute(query_count_orderdetail).fetchone()
        dbr.append("> SELECT COUNT(*) AS c FROM orderdetail ...")
        dbr.append(">>> Volvemos a tener las filas en 'ordertail': " + str(res[0]) + " (0 si el DELETE  habia funcionado)")

        res = db_conn.execute(query_count_orders).fetchone()
        dbr.append("> SELECT COUNT(*) AS c FROM orders ...")
        dbr.append(">>> Volvemos a tener las filas en 'order': " + str(res[0]))

        res = db_conn.execute(query_count_customers).fetchone()
        dbr.append("> SELECT COUNT(*) AS c FROM customers ...")
        dbr.append(">>> Volvemos a tener las filas en 'customers': " + str(res[0]))
    else:
        # TODO: confirmar cambios si todo va bien
        dbr.append("Ejecucion terminada con exito")

    dbConnect()
    return dbr
