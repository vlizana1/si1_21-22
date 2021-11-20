CREATE OR REPLACE FUNCTION setOrderAmount()
    RETURNS void
AS $$
BEGIN
    WITH total_price AS (
        SELECT
          orders.orderid AS ord_id,
          SUM(products.price) AS suma_precio
        FROM
          orders 
          INNER JOIN orderdetail ON
            orders.orderid = orderdetail.orderid
          INNER JOIN products ON
            products.prod_id = orderdetail.prod_id
        GROUP BY orders.orderid)
    UPDATE
        orders
    SET
        netamount = total_price.suma_precio,
        totalamount = total_price.suma_precio * (1 + tax*0.01)
    FROM
        total_price
    WHERE
        orders.orderid = total_price.ord_id AND
        orders.netamount IS NULL;
END;
$$ LANGUAGE plpgsql;

select * from setOrderAmount();
