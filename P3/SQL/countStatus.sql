EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status is null;

EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status = 'Shipped';

create index indexSTTS on orders(status);

EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status is null;

EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status = 'Shipped';

ANALYZE;

EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status is null;

EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status = 'Shipped';

EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status = 'Paid';

EXPLAIN analyze SELECT count(*)
FROM orders
WHERE status = 'Processed';
