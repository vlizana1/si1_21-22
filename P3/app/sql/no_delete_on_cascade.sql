ALTER TABLE orders
ADD FOREIGN KEY (customerid) REFERENCES customers(customerid) ON DELETE NO ACTION;

ALTER TABLE products
ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid) ON DELETE NO ACTION;

ALTER TABLE orderdetail
ADD FOREIGN KEY (orderid) REFERENCES orders(orderid) ON DELETE NO ACTION;

ALTER TABLE orderdetail
ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE NO ACTION;
