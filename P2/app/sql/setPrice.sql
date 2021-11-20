UPDATE
   public.orderdetail 
SET
   price = orderdetail.quantity * new_price.price * POWER (1.02, EXTRACT (YEAR 
FROM
   now()) - EXTRACT (YEAR 
FROM
   orders.orderdate)) 
FROM
   orders, 
   (
      products NATURAL JOIN
         imdb_movies 
   )
   AS new_price 
WHERE
   orders.orderid = orderdetail.orderid 
   AND new_price.prod_id = orderdetail.prod_id;

--actualizamos totalprice(precio total de la suma de la cantidad de un producto)
UPDATE
   public.orderdetail
SET
   price = orderdetail.price*orderdetail.quantity
