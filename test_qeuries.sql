use BarBeerDrinker;

SELECT S1.bar, S1.item, S1.price
	FROM BarBeerDrinker.sells S1, BarBeerDrinker.sells S2
	WHERE S1.item = S2.item & S1.bar != S2.bar