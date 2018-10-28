import re
import math
import random
import source
import csv
import bar_time_rules as btr

# Define paths
fpath_addr = "data/addr.txt"
fpath_phone = "data/phone.txt"
fpath_name = "data/drinkers.txt"
fpath_bars = "data/bars.txt"
fpath_items = "data/items.csv"
fpath_beers = "data/beers.csv"
fpath_brew = "data/breweries.csv"

# random range that can handle empty range
def rand_int_em(start, stop):
	if stop - start == 0:
		return start
	else:
		return random.randint(start, stop)

# picks randomly from a list
def rand_pick(lst):
	return lst[random.randrange(0, len(lst))]

class Time:
	def __init__(self, hour=0, min=0, sec=0):
		if hour < 0 or hour > 23:
			raise ValueError()
		if min < 0 or min > 59:
			raise ValueError()
		if sec < 0 or sec > 59:
			raise ValueError()
		self.hour = hour
		self.min = min
		self.sec = sec
	
	def int_str(self):
		result = ""
		if self.hour < 10:
			result += "0" + str(self.hour)
		else:
			result += str(self.hour)
		if self.min < 10:
			result += "0" + str(self.min)
		else:
			result += str(self.min)
		if self.sec < 10:
			result += "0" + str(self.sec)
		else:
			result += str(self.sec)
		return result
	
	def int_rep(self):
		return int(self.int_str())

def time_from_int_str(int_str):
	hour = int(int_str[0:2])
	minute = int(int_str[2:4])
	sec = int(int_str[4:6])
	return Time(hour, minute, sec)

class Drinker:
	def __init__(self, name="", city="", state="", phone="", addr=""):
		self.name = name
		self.city = city
		self.state = state
		self.phone = phone
		self.addr = addr
	
	def __str__(self):
		return "( name: {0}, city: {1}, state: {2}, phone: {3}, addr: {4} )".format(
			self.name, self.city, self.state, self.phone, self.addr)
	
	def csv(self):
		return '"{0}","{1}","{2}","{3}","{4}"'.format(self.name, self.city, self.state, self.addr, self.phone)

max_drinkers = 1000
def drinkers(count):
	# get source data
	names = source.get_name(fpath_name)
	addrs = source.get_addr(fpath_addr)
	phones = source.get_phone(fpath_phone)

	if (count > max_drinkers or count > len(names) or count > len(addrs) or count > len(phones)):
		raise Exception("Not enough source data")

	# generate
	results = []
	for n in range(count):
		results.append(Drinker(names[n], addrs[n].city, addrs[n].state, phones[n], addrs[n].street))
	return results

# test
# d = drinkers(10)
# for drinker in d:
# 	print(drinker.csv())

class Bar:
	def __init__(self, name="", lisc="", city ="", state="", phone="", addr="", day=0, open_time=Time(), closed_time=Time()):
		self.name = name
		self.license = lisc
		self.city = city
		self.state = state
		self.phone = phone
		self.addr = addr
		self.day = day
		self.open = open_time
		self.closed = closed_time
	
	def is_open(self, day, time):
		if (day != day):
			return False
		open_time = self.open.hour
		close_time = self.closed.hour
		if (close_time < open_time):
			close_time += 24
		if (time.hour < open_time or time.hour >= close_time):
			return False
		return True
	
	def __str__(self):
		return "( name: {0}, license: {1}, city: {2}, state: {3}, phone: {4}, addr: {5} )".format(
			self.name, self.license, self.city, self.state, self.phone, self.addr)
	
	def csv(self):
		return '"{0}", "{1}", "{2}", "{3}", "{4}", "{5}", {6}, "{7}", "{8}"'.format(
			self.name, self.license, self.city, self.state, self.phone, self.addr, self.day, self.open.int_str(), self.closed.int_str())

# generates a random bar time for each day
def bar_time(state):
	same_time_prob = [1, 1, 1, 1, 1, 1, 0] # 6/7 chance same open/close times across different days
	state_time = btr.times[state]
	if not state_time:
		raise ValueError("No entry for state: " + state)
	open_time_hour = state_time[0][0]
	close_time_hour = state_time[1][0]

	# make a time entry for each day
	times = []
	t = 0
	while t < 7:
		same_time = same_time_prob[random.randrange(0, len(same_time_prob))]
		open_time = 0
		close_time = 0
		if not same_time or t == 0:
			# choose random start time
			if (close_time_hour < 0): # if close time not defined, assume open time isn't defined either
				open_time = random.randint(6, 22)
				if open_time+1 < 14:
					close_time = random.randint(14, 6+24)
				else:
					close_time = random.randint(23, 6+24)
			else:
				if open_time_hour >= 0: # if min open hours defined
					if close_time_hour == open_time_hour:
						raise ValueError()
					elif close_time_hour > open_time_hour:
						open_time = rand_int_em(open_time_hour, close_time_hour-1)
						close_time = rand_int_em(open_time+1, close_time_hour)
					else:
						open_time = rand_int_em(open_time_hour, 23)
						close_time = rand_int_em(open_time+1, 24+close_time_hour)
				else: # if only close hours defined
					if close_time_hour < 6:
						open_time = rand_int_em(6, 23)
						close_time = rand_int_em(open_time+1, 24+close_time_hour)
					else:
						open_time = rand_int_em(6, close_time_hour-1)
						close_time = rand_int_em(open_time+1, close_time_hour)
			if open_time > 23:
				open_time = open_time - 24
			if close_time > 23:
				close_time = close_time - 24
		else:
			copy_tar = rand_int_em(0, t-1) # copy a time from a day
			open_time = times[copy_tar][0]
			close_time = times[copy_tar][1]
		
		# cant be open less than 4 hours a day
		if (open_time > close_time):
			if (close_time+24) - open_time >= 4:
				times.append([open_time, close_time])
				t += 1
		else:
			if close_time - open_time >= 4:
				times.append([open_time, close_time])
				t += 1
	return times

max_bars = 218
def bars(count):
	# get source data
	bar_names = source.get_bar(fpath_bars)
	addrs = source.get_addr(fpath_addr, max_drinkers)
	phones = source.get_phone(fpath_phone, max_drinkers)

	if (count > max_bars or count > (99999-10000) or count > len(bar_names) or count > len(addrs) or count > len(phones)):
		raise Exception("Not enough source data")

	lisc_nums = set()

	addr_dict = {} # used to gurauantee at least one bar per state
	more_addr = []
	for addr in addrs:
		if addr.state not in addr_dict:
			addr_dict[addr.state] = addr
		else:
			more_addr.append(addr)
	
	addr_dict_list = list(addr_dict.values())
	if (len(addr_dict_list)) < 50:
		print("warning - not guraunteed bar for each state, length is: " + str(len(addr_dict_list)))

	# generate
	results = []
	for n in range(count):
		# generate license number
		lisc_num = random.randint(10000, 99999)
		while lisc_num in lisc_nums:
			lisc_num = random.randint(10000, 99999)
		lisc_nums.add(lisc_num)

		addr = None
		if n < len(addr_dict_list):
			addr = addr_dict_list[n]
		else:
			addr = more_addr[n - len(addr_dict_list)]

		lisc = addr.state + str(lisc_num)

		hours = bar_time(addr.state)
		for d in range(len(hours)):
			results.append(Bar(bar_names[n], lisc, addr.city, addr.state, phones[n], addr.street,
				d+1, Time(hours[d][0]), Time(hours[d][1])))
	return results

# test
# b = bars(20)
# for bar in b:
# 	print(bar.csv())

def filtr_item(csv_rec):
	for k, v in csv_rec.items():
		if isinstance(v, str) and len(v) > 45:
			return False
	return True

def filtr_beer(csv_rec):
	if (random.random() < 0.75):
		return False
	for k, v in csv_rec.items():
		if k == "name":
			if isinstance(v, str) and len(v) > 45:
				return False
			if k == "name" and not re.match("^['\w\s]*$", v):
				return False
	return True

max_items_stuff = 214
def items_raw(count):
	results = []
	items_count = math.floor(count*0.5)
	if (items_count > max_items_stuff):
		items_count = max_items_stuff
	beers_count = count - items_count
	items = csv.parse_file(fpath_items, items_count, filtr_item)
	for item in items:
		item["type"] = "food"
		results.append(item)

	beers = csv.parse_file(fpath_beers, beers_count, filtr_beer)
	for beer in beers:
		del beer["idx"]
		del beer["abv"]
		del beer["ibu"]
		del beer["id"]
		del beer["style"]
		del beer["ounces"]
		beer["manu"] = csv.retreive(fpath_brew, int(beer["brewery_id"]))["name"]
		del beer["brewery_id"]
		beer["type"] = "beer"
		price = round(float(random.randint(1, 12)) + random.random(), 2)
		beer["highest_price"] = price
		beer["lowest_price"] = price
		results.append(beer)
	return results

class Item:
	def __init__(self, name, item_type, manu=None):
		self.name = name
		self.type = item_type
		self.manu = manu
	
	def csv(self):
		result = '"{0}", "{1}"'.format(self.name, self.type)
		if self.manu:
			result += ', "{0}"'.format(self.manu)
		return result

def items(raw_items):
	results = []
	for item in raw_items:
		result = Item(item["name"], item["type"])
		if "manu" in item:
			result.manu = item["manu"]
		results.append(result)
	return results

# test
# it = items(items_raw(30))
# for item in it:
# 	print(item.csv())

class Frequent:
	def __init__(self, drinker, bar):
		self.drinker = drinker
		self.bar = bar
	
	def csv(self):
		return '"{0}","{1}"'.format(self.drinker, self.bar)

def frequents(drinkers, bars, count):
	results = []
	s = set()
	i = 0
	f = 0
	while True:
		if i >= count:
			break
		drinker = rand_pick(drinkers)
		bar = rand_pick(bars)
		if drinker.state != bar.state: # drinkers cannot frequent bars in different state
			f += 1 # fail attempts
			if (f > count*64):
				break
			continue
		result = (drinker.name, bar.name)
		s.add(result)
		i += 1
	for r in s:
		results.append(Frequent(r[0], r[1]))
	return results

# test
# f = frequents(drinkers(100), bars(100), 50)
# for freq in f:
# 	print(freq.csv())

class Like:
	def __init__(self, drinker, item):
		self.drinker = drinker
		self.item = item
	
	def csv(self):
		return '"{0}","{1}"'.format(self.drinker, self.item)

def likes(drinkers, items, count):
	results = []
	s = set()
	i = 0
	while True:
		if i >= count:
			break
		drinker = rand_pick(drinkers)
		item = rand_pick(items)
		result = (drinker, item.item)
		s.add(result)
		i += 1
	for r in s:
		results.append(Like(r[0], r[1]))
	return results

# test
# l = likes(drinkers(100), items(items_raw(100)), 50)
# for like in l:
# 	print(like.csv())

class Sell:
	def __init__(self, bar, item, price):
		self.bar = bar
		self.item = item
		self.price = float(price)
	
	def csv(self):
		return '"{0}","{1}",{2}'.format(self.bar, self.item, self.price)

def sells(bars, raw_items, min_count):
	results = []
	s = set()
	i = 0
	bar_g_i = 0 # will guraurantee each bar has at least one item
	while True: 
		bar = None
		if i >= min_count:
			if bar_g_i >= len(bars):
				break
			else:
				bar = bars[bar_g_i]
				bar_g_i += 1
		else:
			bar = rand_pick(bars)
		raw_item = rand_pick(raw_items)

		result = (bar.name, raw_item["name"])
		if result not in s:
			s.add(result)

			price = 0
			low_price = float(raw_item["lowest_price"])
			price = low_price
			# if raw_item["type"] == "beer":
			# 	low_price = float(raw_item["lowest_price"])
			# 	high_price = float(raw_item["highest_price"])
			# 	price = round(random.uniform(low_price, high_price), 2)
			# else:
			# 	low_price = float(raw_item["lowest_price"])
			# 	high_price = float(raw_item["highest_price"])
			# 	price = round(random.uniform(low_price, high_price), 2)

			results.append( Sell(bar.name, raw_item["name"], price) )
		i += 1
	return results

# test
# s = sells(bars(100), items_raw(100), 50)
# for sell in s:
# 	print(sell.csv())

# gurauntees that a bar frequented by a drinker has at least 1 item that drinker likes
# def sells_plus(bars, raw_items, count, frequents, likes):
# 	init_sells = sells(bars, raw_items, count)

# 	for freq in frequents:
# 		drinker = freq.drinker
# 		bar = freq.bar

# 		# randomly pick items that the drinker likes (if any)
# 		liked_items = set()
# 		for like in likes:
# 			if like.drinker == drinker:
# 				if len(liked_items) < 1 or random.random() < 0.4:
# 					liked_items.add(like.item)
		
# 		if (len(liked_items) < 1): continue

# 		# find all items sold by the bar
# 		items_sold = set()
# 		for sell in init_sells:
# 			if sell.bar == bar:
# 				items_sold.add(sell.item)

# 		for item in liked_items:
# 			if item not in items_sold:
# 				# search for item in raw_items and generate a price
# 				price = 0
# 				for raw_item in raw_items:
# 					if raw_item["name"] == item:
# 						if raw_item["type"] == "beer":
# 							low_price = 0.75
# 							high_price = 18.00
# 							price = round(random.uniform(low_price, high_price), 2)
# 						else:
# 							low_price = float(raw_item["lowest_price"])
# 							high_price = float(raw_item["highest_price"])
# 							price = round(random.uniform(low_price, high_price), 2)
# 						break
# 				init_sells.append( Sell(bar, item, price) )
# 	return init_sells

# test
# b = bars(100)
# ir = items_raw(100)
# d = drinkers(100)
# s = sells_plus(b, ir, 50, frequents(d, b, 100), likes(d, items(ir), 100))
# for sell in s:
# 	print(sell.csv())

class Transaction:
	def __init__(self, trans_id, bar, drinker, day, time, tip=0, total=0):
		self.trans_id = trans_id
		self.day = day
		self.time = time
		self.bar = bar
		self.drinker = drinker
		self.tip = tip
		self.total = total
	
	def csv(self):
		return '"{0}", {1}, {2}, "{3}", "{4}", {5}, {6}'.format(
			self.trans_id, self.day, self.time.int_str(), self.bar, self.drinker, self.tip, self.total)

# creates transactions for a single drinker
def transactions_drinker(drinker, bars, frequents, likes, sells, count_start, count):
	results = []

	# create a list of bars visited
	d_bars = set()
	for frequent in frequents:
		if frequent.drinker == drinker:
			d_bars.add(frequent.bar)
	
	# everyone should visit at least 2 bars
	if (len(d_bars) < 2):
		add_bars = random.randint(2, 8)
		n = 0
		while n < add_bars:
			bar = rand_pick(bars)
			if bar not in d_bars:
				d_bars.add(bar.name)
				n += 1
	
	# create a list of liked items
	d_likes = set()
	for like in likes:
		if like.drinker == drinker:
			d_likes.add(like.item)
	
	# create a dictionary of bar data
	d_bars_dict = {}
	d_bars_time_dict = {}
	d_sells_dict = {}
	for bar_name in d_bars:
		for bar_i in range(len(bars)):
			bar = bars[bar_i]
			if bar.name == bar_name:
				d_bars_dict[bar_name] = bar

				# create a dictionary of bar times
				for bar_time_day in range(1, 8):
					for bar_time_hour in range(bar.open.hour, bar.closed.hour):
						bar_time_t = (bar_time_day, bar_time_hour)
						if bar_time_t not in d_bars_time_dict:
							d_bars_time_dict[bar_time_t] = []
						d_bars_time_dict[bar_time_t].append(bar_name)

				# create a dictionary of sell data
				for sell in sells:
					if sell.bar == bar_name:
						if bar_name not in d_sells_dict:
							d_sells_dict[bar_name] = []
						d_sells_dict[bar_name].append(sell)
				break
			if bar_i == len(bars)-1:
				print("not found: ", bar_name)

	time_set = set()

	j = 0
	while (j < count):
		# pick a random day+time from available bar times
		time_t = random.choice(list(d_bars_time_dict))
		time_act = Time(time_t[1], random.randint(5, 55), random.randint(0, 59))
		if time_t in time_set:
			continue
		bar_name = rand_pick(d_bars_time_dict[time_t])
		bar_sells = d_sells_dict[bar_name]
		num_bought = rand_int_em(1, len(bar_sells))
		bought_item_names = set()
		bought_items = []
		k = 0
		while k < num_bought:
			rand_item = bar_sells[random.randrange(0, len(bar_sells))]
			if rand_item.item not in bought_item_names:
				bought_item_names.add(rand_item.item)
				bought_items.append(rand_item)
				k += 1

		# calculate tip and total (with tax)
		base_price = 0
		for bought_item in bought_items:
			base_price += bought_item.price
		total = round(base_price * 0.07, 2)
		tip = round(total * (float(random.randint(0, 15))/100.0), 2)

		results.append( (Transaction(count_start+j, bar_name, drinker, time_t[0], time_act, tip, total), bought_item_names) )

		time_set.add(time_t)
		j += 1
	return results


def raw_transactions(drinkers, bars, frequents, likes, sells, count):
	results = []

	if (len(bars) < 12):
		raise Exception("Not enough source data")
	
	d_count = math.ceil(float(count)/float(len(drinkers))) # number of transactions per drinker
	if (d_count > 42):
		raise Exception("Unrealistic transaction count per drinker per week")

		
	# for every drinker
	count_start = 1
	for drinker in drinkers:
		results += transactions_drinker(drinker.name, bars, frequents, likes, sells, count_start, d_count)
		count_start += d_count

	return results

# test
# d = drinkers(100)
# b = bars(100)
# s = sells(b, items_raw(100), 100)
# f = frequents(d, b, 100)
# l = likes(d, s, 100)
# rt = raw_transactions(d, b, f, l, s, 1000)
# print(rt[0:10], len(rt))

class Bill:
	def __init__(self, trans_id, item):
		self.trans_id = trans_id
		self.item = item
	
	def csv(self):
		return '"{0}", "{1}"'.format(self.trans_id, self.item)

def bill_contains(raw_transactions):
	bills = []
	for raw_trans in raw_transactions:
		trans = raw_trans[0]
		items_lst = raw_trans[1]
		for item in items_lst:
			bills.append(Bill(trans.trans_id, item))
	return bills

def transactions(raw_transactions):
	results = []
	for raw_trans in raw_transactions:
		results.append(raw_trans[0])
	return results


# test
# d = drinkers(130)
# b = bars(130)
# s = sells(b, items_raw(250), 1000)
# f = frequents(d, b, 260)
# l = likes(d, s, 260)
# rt = raw_transactions(d, b, f, l, s, 1000)
# bc = bill_contains(rt)
# t = transactions(rt)
# for tr in t[0:20]:
# 	print(tr.csv())