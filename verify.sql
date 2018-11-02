#Detecting transactions after hours
SELECT t.trans_id 
FROM BarBeerDrinker.transaction t
WHERE EXISTS 
        (SELECT b.name 
    FROM BarBeerDrinker.bars b
        WHERE b.name = t.bar & t.time < b.opens & t.time > b.closes)


#Detecting drinkers frequenting out of state
SELECT f.drinker
FROM BarBeerDrinker.frequents f, BarBeerDrinker.bars b, BarBeerDrinker.drinkers d
WHERE f.drinker = d.name & f.bar = b.name & d.state != b.state
#feel like this might be wrong