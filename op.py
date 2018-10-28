# main operating program

import gen
import csv

f_drinkers = "table/drinkers.csv"
f_bars = "table/bars.csv"
f_frequents = "table/frequents.csv"
f_sells = "table/sells.csv"

def write_drinkers_table():
	drinkers = gen.drinkers(gen.max_drinkers)
	f = open(f_drinkers, "w")
	try:
		f.write('name,city,state,addr,phone\n')
		for drinker in drinkers:
			f.write(drinker.csv() + "\n")
	finally:
		f.close()

def read_drinkers_table():
	results = []
	drinkers = csv.parse_file(f_drinkers, gen.max_drinkers)
	for drinker in drinkers:
		results.append(gen.Drinker( drinker["name"], drinker["city"], drinker["state"], drinker["phone"], drinker["addr"] ))
	return results

def write_bars_table():
	bars = gen.bars(gen.max_bars)
	f = open(f_bars, "w")
	try:
		f.write('name,license,city,state,phone,addr,day,open,closed\n')
		for bar in bars:
			f.write(bar.csv() + "\n")
	finally:
		f.close()

def read_bars_table(compress=False):
	results = []
	bars = csv.parse_file(f_bars, gen.max_bars*7)
	for bar in bars:
		if compress:
			if int(bar["day"]) != 1:
				continue
		result = gen.Bar( bar["name"], bar["license"], bar["city"], bar["state"], bar["phone"], bar["addr"],
			int(bar["day"]), gen.time_from_int_str(bar["open"]), gen.time_from_int_str(bar["closed"]) )
		results.append(result)
	return results

def write_frequents_table():
	drinkers = read_drinkers_table()
	bars = read_bars_table(True) # squashed for convenience

	frequents = gen.frequents(drinkers, bars, 2500)
	f = open(f_frequents, "w")
	try:
		f.write('drinker,bar\n')
		for freq in frequents:
			f.write(freq.csv() + "\n")
	finally:
		f.close()

write_frequents_table()

def read_frequents_table():
	results = []
	frequents = csv.parse_file(f_frequents, 2500)
	for freq in frequents:
		result = gen.Frequent( freq["drinker"], freq["bar"] )
		results.append(result)
	return results

# def write_sells_table():
# 	bars = read_bars_table(True) # squashed for convenience
# 	items_raw = gen.items_raw(400)

# 	sells = gen.sells(bars, items_raw, 2500)
# 	f = open(f_sells, "w")
# 	try:
# 		f.write('bar,item,price\n')
# 		for sell in sells:
# 			f.write(sell.csv() + "\n")
# 	finally:
# 		f.close()