DELIMITER |
CREATE TRIGGER trig
BEFORE INSERT ON Inventory_Incl
FOR EACH ROW
BEGIN
SET @tadd = new.ingredient_added_date;
SET @texp = new.ingredient_expiry_date;
IF @tadd > @texp THEN
SET new.ingredient_expiry_date = "1800-1-1";
END IF;
END;