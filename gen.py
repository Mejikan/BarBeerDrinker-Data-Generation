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
		return '"{0}", "{1}", "{2}", "{3}", "{4}"'.format(self.name, self.city, self.state, self.phone, self.addr)

max_drinkers = 150
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
		return '"{0}", "{1}", "{2}", "{3}", "{4}", "{5}", {6}, {7}, {8}'.format(
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

max_bars = 146
def bars(count):
	# get source data
	bar_names = source.get_bar(fpath_bars)
	addrs = source.get_addr(fpath_addr, max_drinkers)
	phones = source.get_phone(fpath_phone, max_drinkers)

	if (count > max_bars or count > (99999-10000) or count > len(bar_names) or count > len(addrs) or count > len(phones)):
		raise Exception("Not enough source data")

	lisc_nums = set()

	# generate
	results = []
	for n in range(count):
		# generate license number
		lisc_num = random.randint(10000, 99999)
		while lisc_num in lisc_nums:
			lisc_num = random.randint(10000, 99999)
		lisc_nums.add(lisc_num)
		lisc = addrs[n].state + str(lisc_num)

		hours = bar_time(addrs[n].state)
		for d in range(len(hours)):
			results.append(Bar(bar_names[n], lisc, addrs[n].city, addrs[n].state, phones[n], addrs[n].street,
				d+1, Time(hours[d][0]), Time(hours[d][1])))
	return results

# test
# b = bars(20)
# for bar in b:
# 	print(bar.csv())

def filtr_item(csv_rec):
	if (random.random() < 0.25):
		return False
	for k, v in csv_rec.items():
		if isinstance(v, str) and len(v) > 45:
			return False
		if k == "last_appeared":
			if not v:
				return False
			if int(v) < 1985 or int(v) > 2018:
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
			if k == "highest_price" or k == "lowest_price":
				if not v:
					return False
				if float(v) <= 0:
					return False
	return True

def items_raw(count):
	results = []
	items_count = math.floor(count*0.5)
	beers_count = count - items_count
	items = csv.parse_file(fpath_items, items_count, filtr_item)
	for item in items:
		del item["id"]
		del item["description"]
		del item["menus_appeared"]
		del item["times_appeared"]
		del item["first_appeared"]
		del item["last_appeared"]
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
		return '"{0}", "{1}"'.format(self.drinker, self.bar)

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
		return '"{0}", "{1}"'.format(self.drinker, self.item)

def likes(drinkers, items, count):
	results = []
	s = set()
	i = 0
	while True:
		if i >= count:
			break
		drinker = rand_pick(drinkers)
		item = rand_pick(items)
		result = (drinker.name, item.name)
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
		self.price = price
	
	def csv(self):
		return '"{0}", "{1}", "{2}"'.format(self.bar, self.item, self.price)

def sells(bars, raw_items, count):
	results = []
	s = set()
	i = 0
	while True:
		if i >= count:
			break
		bar = rand_pick(bars)
		raw_item = rand_pick(raw_items)

		result = (bar.name, raw_item["name"])
		if result not in s:
			s.add(result)

			price = 0
			if raw_item["type"] == "beer":
				low_price = 0.75
				high_price = 18.00
				price = round(random.uniform(low_price, high_price), 2)
			else:
				low_price = float(raw_item["lowest_price"])
				high_price = float(raw_item["highest_price"])
				price = round(random.uniform(low_price, high_price), 2)

			results.append( Sell(bar.name, raw_item["name"], price) )
		i += 1
	return results

# test
# s = sells(bars(100), items_raw(100), 50)
# for sell in s:
# 	print(sell.csv())

# gurauntees that a bar frequented by a drinker has at least 1 item that drinker likes
def sells_plus(bars, raw_items, count, frequents, likes):
	init_sells = sells(bars, raw_items, count)

	for freq in frequents:
		drinker = freq.drinker
		bar = freq.bar

		# randomly pick items that the drinker likes (if any)
		liked_items = set()
		for like in likes:
			if like.drinker == drinker:
				if len(liked_items) < 1 or random.random() < 0.4:
					liked_items.add(like.item)
		
		if (len(liked_items) < 1): continue

		# find all items sold by the bar
		items_sold = set()
		for sell in init_sells:
			if sell.bar == bar:
				items_sold.add(sell.item)

		for item in liked_items:
			if item not in items_sold:
				# search for item in raw_items and generate a price
				price = 0
				for raw_item in raw_items:
					if raw_item["name"] == item:
						if raw_item["type"] == "beer":
							low_price = 0.75
							high_price = 18.00
							price = round(random.uniform(low_price, high_price), 2)
						else:
							low_price = float(raw_item["lowest_price"])
							high_price = float(raw_item["highest_price"])
							price = round(random.uniform(low_price, high_price), 2)
						break
				init_sells.append( Sell(bar, item, price) )
	return init_sells

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

# creates transactions for a single drinker
def transactions_drinker(drinker, bars, frequents, likes, sells, count_start, count):
	results = []

	# create a list of bars visited
	d_bars = set()
	for frequent in frequents:
		if frequent.drinker == drinker.name:
			d_bars.add(frequent.bar)
	
	# everyone should visit at least 4 bars
	if (len(d_bars) < 4):
		add_bars = random.randint(4, 10)
		n = 0
		while n < add_bars:
			bar = rand_pick(bars)
			if bar not in d_bars:
				d_bars.add(bar)
				n += 1
	
	# create a list of liked items
	d_likes = set()
	for like in likes:
		if like.drinker == drinker.name:
			d_likes.add(like.item)
	
	# create a dictionary of bar data
	d_bars_dict = {}
	d_sells_dict = {}
	for bar_name in d_bars:
		for bar in bars:
			if bar.name == bar_name:
				d_bars_dict[bar_name] = bar

				# create a dictionary of sell data
				for sell in sells:
					if sell.bar == bar_name:
						if d_sells_dict[bar_name]:
							pass
						else:
							d_sells_dict[bar_name] = []
						d_sells_dict[bar_name] = sell

				break

	time_set = set()

	j = 0
	while (j < count):
		# pick a random day
		day = random.randint(1, 7)
		hour = random.randint(0, 23)
		time_t = (day, hour)
		time_act = Time(hour, random.randint(5, 55), random.randint(0, 59))
		if time_t in time_set:
			continue
		bar = None
		for bar_name, d_bar in d_bars_dict:
			if d_bar.is_open(day, time_act):
				bar = d_bar
				break
		if not bar:
			continue
		bar_sells = d_sells_dict[bar.name]
		num_bought = rand_int_em(1, len(bar_sells))
		bought_item_names = set()
		bought_items = []
		k = 0
		while k < num_bought:
			rand_item = bar_sells[random.randrange(0, len(bar_sells))]
			if rand_item.name not in bought_item_names:
				bought_item_names.add(rand_item.name)
				bought_items.append(rand_item)
				k += 1

		# calculate tip and total (with tax)
		base_price = 0
		for bought_item in bought_items:
			base_price += bought_item.price
		total = round(base_price * 0.07, 2)
		tip = round(total * (float(random.randint(0, 15))/100.0), 2)

		results.append( (Transaction(count_start+j, bar.name, drinker, day, time_act, tip, total), bought_item_names) )

		time_set.add(time_t)
		j += 1
	return results


def transactions(drinkers, bars, frequents, likes, sells, count):
	results = []

	if (len(bars) < 12):
		raise Exception("Not enough source data")
	
	d_count = math.ceil(float(count)/float(len(drinkers))) # number of transactions per drinker
	if (d_count > 42):
		raise Exception("Unrealistic transaction count per drinker per week")

	i = 1
	while True:
		if i > count:
			break
		
		# for every drinker
		for drinker in drinkers:
			
			transactions_drinker(drinker.name, bars, frequents, likes, sells, i, d_count)

		i += 1

	return results

class Bill:
	def __init__(self, trans_id, item):
		self.trans_id = trans_id
		self.item = item
	
	def csv(self):
		return '"{0}", "{1}"'.format(self.trans_id, self.item)

def bill_contains(sells):
	pass