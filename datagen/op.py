# main operating program

import gen
import csv
import date_transactions as dt

f_drinkers = "table/drinkers.csv"
f_bars = "table/bars.csv"
f_frequents = "table/frequents.csv"
f_items = "table/items.csv"
f_sells = "table/sells.csv"
f_likes = "table/likes.csv"
f_transactions = "table/transactions.csv"
f_transactions2 = "table/transactions2.csv"
f_bill_contains = "table/bill_contains.csv"

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

def read_frequents_table():
	results = []
	frequents = csv.parse_file(f_frequents, 2500)
	for freq in frequents:
		result = gen.Frequent( freq["drinker"], freq["bar"] )
		results.append(result)
	return results

def write_sells_table():
	bars = read_bars_table(True) # squashed for convenience
	items_raw = gen.items_raw(400)

	items = gen.items(items_raw)
	f = open(f_items, "w")
	try:
		f.write('item_name,manufacturer,item_type\n')
		for item in items:
			f.write(item.csv() + "\n")
	finally:
		f.close()

	sells = gen.sells(bars, items_raw, 2500)
	f = open(f_sells, "w")
	try:
		f.write('bar,item,price\n')
		for sell in sells:
			f.write(sell.csv() + "\n")
	finally:
		f.close()

def read_sells_table():
	results = []
	sells = csv.parse_file(f_sells, 3000)
	for sell in sells:
		result = gen.Sell( sell["bar"], sell["item"], sell["price"] )
		results.append(result)
	return results

def write_likes_table():
	drinkers = read_drinkers_table()
	frequents = read_frequents_table()
	sells = read_sells_table()

	likes = gen.likes(drinkers, frequents, sells, 3000)
	f = open(f_likes, "w")
	try:
		f.write('drinker,item\n')
		for like in likes:
			f.write(like.csv() + "\n")
	finally:
		f.close()

def read_likes_table():
	results = []
	likes = csv.parse_file(f_likes, 10000)
	for like in likes:
		result = gen.Like( like["drinker"], like["item"] )
		results.append(result)
	return results

def write_transactions_table():
	drinkers = read_drinkers_table()
	bars = read_bars_table()
	frequents = read_frequents_table()
	likes = read_likes_table()
	sells = read_sells_table()

	rt = gen.raw_transactions(drinkers, bars, frequents, likes, sells, 20000)

	transactions = gen.transactions(rt)
	f = open(f_transactions, "w")
	try:
		f.write('trans_id,day,time,bar,drinker,tip,total\n')
		for trans in transactions:
			f.write(trans.csv() + "\n")
	finally:
		f.close()

	bills = gen.bill_contains(rt)
	f = open(f_bill_contains, "w")
	try:
		f.write('trans_id,item\n')
		for bill in bills:
			f.write(bill.csv() + "\n")
	finally:
		f.close()

def read_transactions_table():
	results = []
	transactions = csv.parse_file(f_transactions, 20000)
	for trans in transactions:
		result = gen.Transaction( trans["trans_id"], trans["bar"], trans["drinker"], int(trans["day"]), gen.time_from_int_str(trans["time"]), float(trans["tip"]), float(trans["total"]) )
		results.append(result)
	return results

# transaction stuff
def write_transactions_date():
	results = []
	transactions = read_transactions_table()
	for trans in transactions:
		date = dt.rand_date(trans.day)
		date = date.replace(hour=trans.time.hour, minute=trans.time.min, second=trans.time.sec)
		results.append(gen.ChronoTransaction( trans.trans_id, trans.bar, trans.drinker, date, trans.day, trans.time, trans.tip, trans.total ))

	transactions = results

	f = open(f_transactions2, "w")
	try:
		f.write('trans_id,day,time,date,bar,drinker,tip,total\n')
		for trans in transactions:
			f.write(trans.csv() + "\n")
	finally:
		f.close()

#write_drinkers_table()
#write_bars_table()
#write_frequents_table()

#write_sells_table()
#write_likes_table()
#write_transactions_table()

write_transactions_date()

