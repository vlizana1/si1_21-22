ALTER TABLE customers ADD COLUMN promo decimal(4,2) DEFAULT 0;

CREATE OR REPLACE FUNCTION promocion()
  RETURNS TRIGGER
AS $$
BEGIN
    PERFORM pg_sleep(5);
    
    UPDATE orders
    SET netamount = (netamount *(100 - new.promo))/ 100
    WHERE customerid = NEW.customerid;
    
    RETURN new;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS descuento
  ON customers;

CREATE TRIGGER descuento
  AFTER UPDATE OF promo
  ON customers
  FOR EACH ROW EXECUTE PROCEDURE promocion();

BEGIN;

UPDATE customers
  SET promo=1
  WHERE customerid=5;

COMMIT;
