use BarBeerDrinker;

DELIMITER $$

CREATE TRIGGER assert2_update BEFORE UPDATE
ON BarBeerDrinker.frequents
FOR EACH ROW
BEGIN
	DECLARE MSG VARCHAR(128);
    IF (new.bar IS NULL) THEN
		SET msg = concat('"bar" field cannot be empty');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	ELSEIF (new.drinker IS NULL) THEN
		SET msg = concat('"drinker" field cannot be empty');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    ELSEIF (SELECT NOT EXISTS (
		SELECT *
		FROM BarBeerDrinker.bars b, BarBeerDrinker.drinkers d
		WHERE d.name = new.drinker && b.name = new.bar && b.state = d.state
	)) THEN
		SET msg = concat('UPDATE not accepted due to violation of assertion 2.');
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	END IF;
END$$

DELIMITER ;

