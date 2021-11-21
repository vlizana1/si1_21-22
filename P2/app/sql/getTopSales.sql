CREATE 
OR REPLACE FUNCTION getTopSales(year1 INTEGER, year2 INTEGER) 
    RETURNS TABLE(year INTEGER,
                  pelicula CHARACTER VARYING(255),
                  ventas INTEGER)
    AS $$ 
    BEGIN
        RETURN QUERY( 
            SELECT aux2.year :: INTEGER, 
                   imdb_movies.movietitle, 
                   aux2.ventas :: INTEGER
            FROM (SELECT aux1.year,
                         (ARRAY_AGG(aux1.movieid ORDER BY aux1.ventas DESC)) [1] AS movieid,
                         MAX(aux1.ventas) AS ventas 
                  FROM (SELECT EXTRACT(year FROM orderdate) AS year,
                               movieid,
                               SUM(quantity) AS ventas 
                        FROM (orders INNER JOIN orderdetail ON orders.orderid = orderdetail.orderid ) AS T INNER JOIN
                             products ON T.prod_id = products.prod_id 
                        GROUP BY year,
                                 movieid) AS aux1 
                  GROUP BY aux1.year) AS aux2 INNER JOIN
                 imdb_movies ON aux2.movieid = imdb_movies.movieid 
            WHERE aux2.year >= $1 
              AND aux2.year <= $2 
            ORDER BY aux2.ventas DESC);
    END;
$$ language plpgsql;

SELECT * FROM getTopSales(1970, 1980)
