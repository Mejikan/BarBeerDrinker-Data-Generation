use BarBeerDrinker;

DELIMITER $$

CREATE TRIGGER id_check BEFORE INSERT
ON BarBeerDrinker.test
FOR EACH ROW
BEGIN
	DECLARE MSG VARCHAR(128);
	IF (new.id > 500) THEN
		SET msg = concat('ID larger than 500 not allowed LOL', CAST(new.id AS CHAR));
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	END IF;
END$$

DELIMITER ;

#################

SELECT COUNT(*) AS CNT FROM BarBeerDrinker.test
WHERE drinker = 'larvin';

SELECT EXISTS (
	SELECT * FROM BarBeerDrinker.test
	WHERE drinker = 'pop'
)

################

DELIMITER $$

CREATE TRIGGER q_check BEFORE INSERT
ON BarBeerDrinker.test
FOR EACH ROW
BEGIN
	DECLARE MSG VARCHAR(128);
	IF (SELECT EXISTS (
		SELECT * FROM BarBeerDrinker.test
		WHERE drinker = new.drinker
	))
    THEN
		SET msg = concat('ID larger than 500 not allowed LOL', CAST(new.id AS CHAR));
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	END IF;
END$$

DELIMITER ;