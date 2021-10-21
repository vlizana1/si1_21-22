import sys
import traceback
import datetime
from sqlalchemy import MetaData
from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:"
                          "alumnodb@localhost/si1",
                          echo=False)
db_meta = MetaData(bind=db_engine)




def getTopVentasLast3Years():
    currentDateTime = datetime.datetime.now()
    date = currentDateTIme.date()
    year = int(date.year)
    try:
        db_conn = None
        db_conn = db_engine.connect()
        list_movies = list(db_conn.execute(
            "SELECT movieid, f.year, ventas, pelicula FROM "
            "getTopVentas(2019,2021) as f ,"
#            "getTopVentas(" + str(year-2) + "," + str(year) + ") as f ,"
            " imdb_movies WHERE pelicula=movietitle"))
        db_conn.close()
        return list_movies
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'



def set_income(customerid, saldo_aumento):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_conn.execute("UPDATE customers SET income = "
                        + str(saldo_aumento) +
                        " WHERE customerid = "
                        + str(customerid))
        db_conn.close()
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def get_languages():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        list_languages = list(db_conn.execute("SELECT * FROM languages "
                                              "ORDER BY language"))
        db_conn.close()
        return list_languages

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def get_countries():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        countries = list(db_conn.execute("SELECT * FROM countries "
                                         "ORDER BY country"))
        db_conn.close()
        return countries
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'

def get_movies_years():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        list_movies_years = list(db_conn.execute("SELECT DISTINCT year"
                                                 " FROM imdb_movies"
                                                 " ORDER BY year"))
        db_conn.close()
        return list_movies_years

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def get_movies_by_year(year):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        list_movies_year = list(db_conn.execute("SELECT * FROM imdb_movies"
                                                " WHERE year = " + str(year)))
        db_conn.close()
        return list_movies_by_year

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'




def create_user(username, password, email, credit_card,
                cvv, expiration_month, expiration_year,
                credit_card_type, owner, saldo):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        customer_id = list(db_conn.execute("SELECT MAX(customerid) "
                                           "as c FROM customers"))
        customer_id = int(customer_id[0].c) + 1
        creditcard_id = list(db_conn.execute("SELECT MAX(creditcard_id)"
                                             " as c FROM creditcards"))

        creditcard_id = creditcard_id[0].c + 1

        query = "INSERT INTO creditcards" \
                "(creditcard_id," \
                "creditcard," \
                "creditcardtype," \
                "creditcardexpiration," \
                "cvv" \
                ") VALUES("
        query += str(creditcard_id)
        query += ",'"
        query += str(credit_card)
        query += "','"
        query += str(credit_card_type)
        query += "','"
        query += str(expiration_month + expiration_year)
        query += "','"
        query += str(cvv)
        query += "')"
        db_conn.execute(query)

        query_customer = "INSERT INTO customers" \
                         " (customerid," \
                         "firstname," \
                         "lastname," \
                         "address1," \
                         "city," \
                         "country," \
                         "zip," \
                         " email," \
                         "username," \
                         "password," \
                         "income," \
                         "creditcard_id" \
                         ") VALUES("
        query_customer += str(customer_id)
        query_customer += ",'"
        query_customer += owner[0]
        query_customer += "','"
        query_customer += owner[1]
        query_customer += "',"
        query_customer += "'EPS','Madrid','España',28049,'"
        query_customer += email
        query_customer += "','"
        query_customer += username
        query_customer += "','"
        query_customer += password
        query_customer += "',"
        query_customer += str(saldo)
        query_customer += ","
        query_customer += str(creditcard_id)
        query_customer += ")"
        db_conn.execute(query_customer)
        db_conn.close()
        return get_customer(username, password)

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def get_order_carrito(user_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        order = list(db_conn.execute(
            "SELECT orderid as c FROM orders "
            "WHERE customerid = " + str(user_id) +
            " and status = 'carrito'"))
        db_conn.close()

        if order == []:
            order = create_order(user_id)
        else:
            order = int(order[0].c)
        return order

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def create_order(user_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        order_id = list(db_conn.execute("SELECT "
                                        "MAX(orderid) "
                                        "as c FROM orders"))
        order_id = int(order_id[0].c) + 1

        query = "insert into orders " \
                "(orderid, customerid," \
                " orderdate, netamount," \
                " totalamount, " \
                "status) " \
                "values (" \
                + str(order_id) + \
                ", " + str(user_id) + \
                ", now()," \
                "0, 0," \
                "'carrito')"
        db_conn.execute(query)
        db_conn.close()
        return order_id

    except Exception:

        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def insert_order(user_id, prod_id, price, quantity):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        order_id = get_order_carrito(user_id)

        query = list(db_conn.execute(
            "SELECT COUNT(*) AS c FROM orderdetail "
            "WHERE orderid = " + str(order_id) +
            " AND prod_id = " + str(prod_id)))

        num_prod = int(query[0].c)

        if num_prod == 0:
            totalprice = round(price * quantity, 2)
            db_conn.execute("INSERT INTO orderdetail("
                            "orderid, prod_id, price,"
                            " quantity, totalprice) "
                            "VALUES (" + str(order_id) +
                            ", " + str(prod_id) + ", " +
                            str(price) + ", " +
                            str(quantity) + ", " +
                            str(totalprice) + ")")
        else:
            old_quantity = list(db_conn.execute(
                "SELECT quantity as c FROM "
                "orderdetail WHERE orderid = " + str(order_id) +
                " AND prod_id = " + str(
                    prod_id)))
            new_quantity = int(old_quantity[0].c) + quantity
            totalprice = round(price * new_quantity, 2)
            db_conn.execute("UPDATE orderdetail SET quantity = "
                            + str(new_quantity) + " WHERE orderid = "
                            + str(order_id) + " AND prod_id = " + str(prod_id))
            db_conn.execute("UPDATE orderdetail SET totalprice ="
                            + str(totalprice) + " WHERE orderid = "
                            + str(order_id) + " AND prod_id = " + str(prod_id))
        db_conn.close()

    except Exception:

        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def get_order_user(user_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        result = list(db_conn.execute(
            "SELECT * FROM orders NATURAL JOIN orderdetail NATURAL JOIN "
            "products NATURAL JOIN imdb_movies WHERE orderid = " + str(
                get_order_carrito(user_id)) + "ORDER BY movietitle"))

        db_conn.close()

        return result
    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def add_carrito(user_id, prod_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        order_id = get_order_carrito(user_id)
        old_quantity = list(db_conn.execute(
            "SELECT quantity as c FROM orderdetail WHERE orderid = "
            + str(order_id) + " AND prod_id = " + str(prod_id)))
        price = list(db_conn.execute(
            "SELECT price as p FROM orderdetail WHERE orderid = "
            + str(order_id) + " AND prod_id = " + str(prod_id)))
        new_quantity = int(old_quantity[0].c) + 1

        totalprice = round(price[0].p * new_quantity, 2)
        db_conn.execute("UPDATE orderdetail SET quantity = "
                        + str(new_quantity) + " WHERE orderid = "
                        + str(order_id) +
                        " AND prod_id = " + str(prod_id))
        db_conn.execute("UPDATE orderdetail SET totalprice ="
                        + str(totalprice) + " WHERE orderid = " + str(order_id)
                        + " AND prod_id = " + str(prod_id))
        db_conn.close()

    except Exception:

        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'

def remove_carrito(user_id, prod_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        order_id = get_order_carrito(user_id)
        old_quantity = list(db_conn.execute(
            "SELECT quantity as c FROM orderdetail WHERE orderid = "
            + str(order_id) + " AND prod_id = " + str(prod_id)))
        price = list(db_conn.execute(
            "SELECT price as p FROM orderdetail WHERE orderid = "
            + str(order_id) + " AND prod_id = " + str(prod_id)))
        new_quantity = int(old_quantity[0].c) - 1
        if new_quantity == 0:
            db_conn.execute("DELETE FROM orderdetail WHERE orderid = "
                            + str(order_id) + " AND prod_id = " + str(prod_id))

        totalprice = round(price[0].p * new_quantity, 2)
        db_conn.execute("UPDATE orderdetail SET quantity = "
                        + str(new_quantity) + " WHERE orderid = "
                        + str(order_id) +
                        " AND prod_id = " + str(prod_id))
        db_conn.execute("UPDATE orderdetail SET totalprice ="
                        + str(totalprice) + " WHERE orderid = " + str(order_id)
                        + " AND prod_id = " + str(prod_id))
        db_conn.close()

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def comprar(customerid, saldo):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        products = list(db_conn.execute("SELECT quantity,stock,"
                                        "description,movietitle "
                                        " FROM orderdetail NATURAL JOIN"
                                        " orders NATURAL JOIN inventory"
                                        " NATURAL JOIN products NATURAL JOIN "
                                        " imdb_movies WHERE"
                                        " customerid = " + str(customerid) +
                                        " AND status='carrito' "
                                        "AND quantity > stock"))
        if products:
            return products

        db_conn.execute("UPDATE customers set income = "
                        + str(saldo) + " where customerid = "
                        + str(customerid))
        db_conn.execute("UPDATE orders set status = 'Paid' "
                        "where customerid = " + str(customerid)
                        + "and status = 'carrito'")
        db_conn.close()

    except Exception:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'


def get_historial(user_id):
    try:
        db_conn = None
        db_conn = db_engine.connect()
        orderids = list(db_conn.execute(
            "SELECT orderid AS id FROM orders WHERE customerid = "
            + str(user_id) + " AND status != 'carrito'"))
        orders = []
        order_ele = []
        for order in orderids:
            new_order = int(order.id)
            counter_orderdetail = list(db_conn.execute(
                "SELECT count(*) as c FROM orders NATURAL JOIN orderdetail"
                " NATURAL JOIN products NATURAL JOIN imdb_movies"
                " WHERE orderid = " + str(new_order)))[0]
            if int(counter_orderdetail.c) != 0:
                counter_orderdetail = int(counter_orderdetail.c)
                order_element = list(db_conn.execute(
                    "SELECT * FROM orders NATURAL JOIN orderdetail "
                    "NATURAL JOIN products NATURAL JOIN imdb_movies"
                    " WHERE orderid = " + str(new_order) +
                    " ORDER BY orderdate DESC"))
                for o in range(0, counter_orderdetail):
                    order_dict = {'order_detail': order_element[o]}
                    order_ele.append(order_dict)
                    order_dict = None

                orders_dict = {'order': order_ele}
                orders.append(orders_dict)
                order_ele = []
        db_conn.close()
        return orders

    except Exception:

        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-" * 60)
        traceback.print_exc(file=sys.stderr)
        print("-" * 60)

        return 'ERR'
