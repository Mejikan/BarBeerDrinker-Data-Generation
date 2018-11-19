SELECT DISTINCT post1.item FROM
	(SELECT DISTINCT base4.item FROM
		(SELECT s3.* FROM BarBeerDrinker.sells s3,
		(SELECT DISTINCT bar FROM BarBeerDrinker.sells s2
		WHERE s2.item = 'Arjuna') b2
		WHERE b2.bar = s3.bar) base3,
		(SELECT s3.* FROM BarBeerDrinker.sells s3,
		(SELECT DISTINCT bar FROM BarBeerDrinker.sells s2
		WHERE s2.item = 'Arjuna') b2
		WHERE b2.bar = s3.bar) base4
	WHERE base3.bar = base4.bar AND base3.item = 'Arjuna' AND base4.item <> 'Arjuna' AND base3.price < base4.price) post1
WHERE post1.item IN
	(SELECT DISTINCT base2.item FROM
		(SELECT s1.* FROM BarBeerDrinker.sells s1,
		(SELECT DISTINCT bar FROM BarBeerDrinker.sells s0
		WHERE s0.item = 'Arjuna') b0
		WHERE b0.bar = s1.bar) base1,
		(SELECT s1.* FROM BarBeerDrinker.sells s1,
		(SELECT DISTINCT bar FROM BarBeerDrinker.sells s0
		WHERE s0.item = 'Arjuna') b0
		WHERE b0.bar = s1.bar) base2
	WHERE base1.bar = base2.bar AND base1.item = 'Arjuna' AND base2.item <> 'Arjuna' AND base1.price > base2.price);