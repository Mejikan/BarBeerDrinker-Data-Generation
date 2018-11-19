use BarBeerDrinker;

DELIMITER $$

CREATE TRIGGER assert1_insert BEFORE INSERT
ON BarBeerDrinker.transactions
FOR EACH ROW
BEGIN
	DECLARE MSG VARCHAR(128);
    IF (new.bar IS NULL) THEN
		SET msg = concat('"bar" field cannot be empty');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	ELSEIF (new.date IS NULL) THEN
		SET msg = concat('"date" field cannot be empty');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    ELSEIF (SELECT EXISTS (
		SELECT *
			FROM BarBeerDrinker.transactions t, (SELECT h.*, IF(hour(h.closes) < hour(h.opens), 1, 0) AS flag FROM BarBeerDrinker.hours h) h
			WHERE (
            ( h.flag = 0 && (( hour(time(t.date)) >= hour(h.closes) || hour(time(new.date)) < hour(h.opens) )
				&& h.bar = new.bar && (h.day-1) = dayofweek(new.date)) ) OR
			( h.flag = 1 && (( hour(time(new.date)) >= hour(h.closes) && hour(time(new.date)) < hour(h.opens) )
				&& h.bar = new.bar && (h.day-1) = dayofweek(new.date)) ) )
	)) THEN
		SET msg = concat('INSERT not accepted due to violation of assertion 1.');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	END IF;
END$$

DELIMITER ;

