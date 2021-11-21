CREATE OR REPLACE FUNCTION updInventory() RETURNS TRIGGER AS $$
    DECLARE
        prod RECORD;
    BEGIN
        IF (NEW.status = 'Paid') THEN
            FOR prod IN (SELECT prod_id, orderid, quantity
                         FROM orderdetail
                         WHERE orderid = NEW.orderid) LOOP
                UPDATE inventory
                    SET sales = sales + prod.quantity,
                        stock = stock - prod.quantity
                    WHERE prod_id = prod.prod_id;
            END LOOP;
        END IF;
        
        UPDATE customers
            SET balance = balance - NEW.totalamount
            WHERE customerid = NEW.customerid;
        
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION updAlerts() RETURNS TRIGGER AS $$
    BEGIN
        IF (NEW.stock <= 0) AND (OLD.stock > 0) THEN
            INSERT INTO alerts (prod_id, fecha)
                VALUES (NEW.prod_id, CURRENT_TIMESTAMP);
        END IF;
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS updInventory ON orders;
CREATE TRIGGER updInventory
    AFTER UPDATE
    ON orders
    FOR EACH ROW EXECUTE PROCEDURE updInventory();


DROP TRIGGER IF EXISTS updAlerts ON inventory;
CREATE TRIGGER updAlerts
    AFTER UPDATE
    ON inventory
    FOR EACH ROW EXECUTE PROCEDURE updAlerts();
