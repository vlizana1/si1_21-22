ALTER TABLE imdb_actormovies
ADD PRIMARY KEY (actorid, movieid);

--se añaden las foreign keys--
ALTER TABLE imdb_actormovies
ADD FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid) ON DELETE CASCADE;

ALTER TABLE imdb_actormovies
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid) ON DELETE CASCADE;

ALTER TABLE orderdetail
ADD FOREIGN KEY (orderid) REFERENCES orders(orderid) ON DELETE CASCADE;

ALTER TABLE orderdetail
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE;

ALTER TABLE inventory
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id)ON DELETE CASCADE;

ALTER TABLE orders
ADD FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE CASCADE;

ALTER TABLE products
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid) ON DELETE CASCADE;


--se ajusta el precio a dos decimales
ALTER TABLE orderdetail
ALTER COLUMN price TYPE numeric(10,2);

--se ajusta el precio total a dos decimales
ALTER TABLE orders
ALTER COLUMN totalamount TYPE numeric(10,2);

--se ajusta el precio neto a dos decimales
ALTER TABLE orders
ALTER COLUMN netamount TYPE numeric(10,2);


--cambiamos el genero de malea M y de  female a F para que sea equivalente al establecido en la tabla customer
UPDATE imdb_actors SET gender='M' WHERE gender='male';
UPDATE imdb_actors SET gender='F' WHERE gender='female';
ALTER TABLE imdb_actors ALTER gender TYPE character varying(1);

--Eliminamos numpartitipation como PK y dejamos solo directorid,movieid en directormovies
ALTER TABLE imdb_directormovies DROP CONSTRAINT imdb_directormovies_pkey;
ALTER TABLE imdb_directormovies ADD CONSTRAINT imdb_directormovies_pkey PRIMARY KEY (directorid, movieid);


--Eliminamos  NOT NULL de movierelease en movies
ALTER TABLE imdb_movies ALTER COLUMN movierelease DROP NOT NULL;


--Eliminamos not null de aquellos campos de customer inecesarios para nuestra web
ALTER TABLE customers ALTER firstname DROP NOT NULL;
ALTER TABLE customers ALTER lastname DROP NOT NULL;
ALTER TABLE customers ALTER address1 DROP NOT NULL;
ALTER TABLE customers ALTER city DROP NOT NULL;
ALTER TABLE customers ALTER country DROP NOT NULL;
ALTER TABLE customers ALTER region DROP NOT NULL;
ALTER TABLE customers ALTER creditcardtype DROP NOT NULL;
ALTER TABLE customers ALTER creditcardexpiration DROP NOT NULL;--no entiendo como funciona el numero



--saldo del cliente, con dos decimales
ALTER TABLE customers ALTER income SET NOT NULL;
ALTER TABLE customers ALTER COLUMN income TYPE numeric(10,2);


--Anadimos unique y not null a email de customer
ALTER TABLE customers
ADD CONSTRAINT email_unique
UNIQUE (email);

ALTER TABLE customers
ALTER COLUMN email SET  NOT NULL;

-- add new columns

ALTER TABLE customers 
ADD COLUMN loyalty numeric
default 0;

ALTER TABLE customers 
ADD COLUMN balance bigint;


---add language table
CREATE TABLE public.alerts(
    alertid serial PRIMARY KEY NOT NULL,
    prod_id integer NOT NULL,
    fecha timestamp NOT NULL
);

ALTER TABLE alerts
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE;

SET timezone to 'Europe/Paris';


-- new funcs

CREATE FUNCTION setCustomersBalance(IN initialBalance bigint)
RETURNS BIGINT AS $$
	UPDATE customers
		SET balance = ((random() * ($1 - 0)) + 0) 
	RETURNING balance;
$$ LANGUAGE SQL;

SELECT * FROM setCustomersBalance(100);

