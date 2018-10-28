# main operating program

import gen

f_drinkers = "table/drinkers.csv"
f_bars = "table/bars.csv"

def write_drinkers_table():
	drinkers = gen.drinkers(gen.max_drinkers)
	f = open(f_drinkers, "w")
	try:
		f.write('name,city,state,addr,phone\n')
		for drinker in drinkers:
			f.write(drinker.csv() + "\n")
	finally:
		f.close()

def write_bars_table():
	bars = gen.bars(gen.max_bars)
	f = open(f_bars, "w")
	try:
		f.write('name,license,city,state,phone,addr,day,open,closed\n')
		for bar in bars:
			f.write(bar.csv() + "\n")
	finally:
		f.close()

write_bars_table()