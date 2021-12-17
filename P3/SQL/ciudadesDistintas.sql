drop index if exists indexTA
create index indexTA on customers(creditcardtype);


EXPLAIN analyze SELECT count (distinct customers.city)
FROM orders, customers
WHERE orders.customerid = customers.customerid
  AND extract(year FROM orderdate) = 2016
  AND extract(month FROM orderdate) = 04
  AND creditcardtype = 'VISA';

/*
SELECT count (distinct customers.city)
FROM orders, customers
WHERE orders.customerid = customers.customerid
  AND extract(year from orderdate) = 2016
  AND extract(month from orderdate) = 04
  AND creditcardtype = 'VISA';
  */
