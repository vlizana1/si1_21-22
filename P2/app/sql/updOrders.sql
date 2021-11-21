CREATE OR REPLACE FUNCTION updOrders() RETURNS TRIGGER AS $$
    DECLARE
        price integer;
        id integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            price = NEW.quantity * NEW.price;
            id = NEW.orderid;
        ELSIF (TG_OP = 'UPDATE') THEN
            price = (NEW.quantity * NEW.price) - (OLD.quantity * OLD.price);
            id = NEW.orderid;
        ELSIF (TG_OP = 'DELETE') THEN
            price = 0 - (OLD.quantity * OLD.price);
            id = OLD.orderid;
        END IF;
        
        UPDATE orders
            SET netamount = netamount + price
            WHERE orderid = id;
        
        UPDATE orders
            SET totalamount = netamount * ((tax * 0.01) + 1)
            WHERE orderid = id;
        
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS updOrders ON orderdetail;
CREATE TRIGGER updOrders
    AFTER INSERT
       OR UPDATE
       OR DELETE
    ON orderdetail
    FOR EACH ROW EXECUTE PROCEDURE updOrders();
