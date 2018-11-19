use BarBeerDrinker;

DELIMITER $$

CREATE TRIGGER assert3_insert AFTER INSERT
ON BarBeerDrinker.sells
FOR EACH ROW
BEGIN
	DECLARE MSG VARCHAR(128);
    IF (new.bar IS NULL) THEN
		SET msg = concat('"bar" field cannot be empty');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	ELSEIF (new.item IS NULL) THEN
		SET msg = concat('"item" field cannot be empty');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    ELSEIF (SELECT EXISTS (
		SELECT DISTINCT post1.item FROM
			(SELECT DISTINCT base4.item FROM
				(SELECT s3.* FROM BarBeerDrinker.sells s3,
				(SELECT DISTINCT bar FROM BarBeerDrinker.sells s2
				WHERE s2.item = new.item) b2
				WHERE b2.bar = s3.bar) base3,
				(SELECT s3.* FROM BarBeerDrinker.sells s3,
				(SELECT DISTINCT bar FROM BarBeerDrinker.sells s2
				WHERE s2.item = new.item) b2
				WHERE b2.bar = s3.bar) base4
			WHERE base3.bar = base4.bar AND base3.item = new.item AND base4.item <> new.item AND base3.price < base4.price) post1
		WHERE post1.item IN
			(SELECT DISTINCT base2.item FROM
				(SELECT s1.* FROM BarBeerDrinker.sells s1,
				(SELECT DISTINCT bar FROM BarBeerDrinker.sells s0
				WHERE s0.item = new.item) b0
				WHERE b0.bar = s1.bar) base1,
				(SELECT s1.* FROM BarBeerDrinker.sells s1,
				(SELECT DISTINCT bar FROM BarBeerDrinker.sells s0
				WHERE s0.item = new.item) b0
				WHERE b0.bar = s1.bar) base2
			WHERE base1.bar = base2.bar AND base1.item = new.item AND base2.item <> new.item AND base1.price > base2.price)
	)) THEN
		SET msg = concat('INSERT not accepted due to violation of assertion 3.');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	END IF;
END$$

DELIMITER ;

