CREATE OR REPLACE FUNCTION updInventory() RETURNS TRIGGER AS $$
DECLARE
    product record;
BEGIN

CREATE TABLE tabla_aux(
    prod_id INTEGER
);
INSERT INTO tabla_aux
    SELECT prod_id AS product FROM orderdetail WHERE orderdetail.orderid = new.orderid;


IF (new.status = 'Paid') THEN
    UPDATE
        inventory
    SET
        sales = sales + orderdetail.quantity,
        stock = stock - orderdetail.quantity
    FROM
        orderdetail, tabla_aux
    WHERE
        orderdetail.prod_id = tabla_aux.prod_id;
    INSERT INTO alerts (prod_id)
        SELECT prod_id FROM inventory NATURAL JOIN orderdetail, tabla_aux WHERE (inventory.stock = 0 AND inventory.prod_id=tempo.prod_id AND orderid=new.orderid);
	UPDATE 
		alerts
	SET 
		fecha = CURRENT_TIMESTAMP;
	FROM inventory NATURAL JOIN orderdetail, tabla_aux 
	WHERE inventory.prod_id= alerts.prod_id;
END IF;

DROP TABLE tabla_aux;

RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS updInventory ON orders;
CREATE TRIGGER updInventory AFTER UPDATE ON orders
FOR EACH ROW EXECUTE PROCEDURE updInventory();