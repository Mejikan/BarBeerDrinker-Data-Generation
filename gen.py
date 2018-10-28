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
def rand_range_em(start, stop):
	if stop - start == 0:
		return start
	else:
		return random.randrange(start, stop)

# picks randomly from a list
def rand_pick(lst):
	return lst[random.randrange(0, len(lst))]

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
	def __init__(self, name="", lisc="", city ="", state="", phone="", addr="", day=0, open_time=0, closed_time=0):
		self.name = name
		self.license = lisc
		self.city = city
		self.state = state
		self.phone = phone
		self.addr = addr
		self.day = day
		self.open = open_time
		self.closed = closed_time
	
	def __str__(self):
		return "( name: {0}, license: {1}, city: {2}, state: {3}, phone: {4}, addr: {5} )".format(
			self.name, self.license, self.city, self.state, self.phone, self.addr)
	
	def csv(self):
		return '"{0}", "{1}", "{2}", "{3}", "{4}", "{5}", {6}, {7}, {8}'.format(
			self.name, self.license, self.city, self.state, self.phone, self.addr, self.day, self.open, self.closed)

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
				open_time = random.randrange(6, 22)
				if open_time+1 < 14:
					close_time = random.randrange(14, 6+24)
				else:
					close_time = random.randrange(23, 6+24)
			else:
				if open_time_hour >= 0: # if min open hours defined
					if close_time_hour == open_time_hour:
						raise ValueError()
					elif close_time_hour > open_time_hour:
						open_time = rand_range_em(open_time_hour, close_time_hour-1)
						close_time = rand_range_em(open_time+1, close_time_hour)
					else:
						open_time = rand_range_em(open_time_hour, 23)
						close_time = rand_range_em(open_time+1, 24+close_time_hour)
				else: # if only close hours defined
					if close_time_hour < 6:
						open_time = rand_range_em(6, 23)
						close_time = rand_range_em(open_time+1, 24+close_time_hour)
					else:
						open_time = rand_range_em(6, close_time_hour-1)
						close_time = rand_range_em(open_time+1, close_time_hour)
			if open_time > 23:
				open_time = open_time - 24
			if close_time > 23:
				close_time = close_time - 24
		else:
			copy_tar = rand_range_em(0, t-1) # copy a time from a day
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
		lisc_num = random.randrange(10000, 99999)
		while lisc_num in lisc_nums:
			lisc_num = random.randrange(10000, 99999)
		lisc_nums.add(lisc_num)
		lisc = addrs[n].state + str(lisc_num)

		hours = bar_time(addrs[n].state)
		for d in range(len(hours)):
			results.append(Bar(bar_names[n], lisc, addrs[n].city, addrs[n].state, phones[n], addrs[n].street, d+1, hours[d][0], hours[d][1]))
	return results

# test
# b = bars(20)
# for bar in b:
# 	print(bar.csv())

def items_raw(count):
	results = []
	items_count = math.floor(count*0.5)
	beers_count = count - items_count
	items = csv.parse_file(fpath_items, items_count, 0.25)
	for item in items:
		del item["id"]
		del item["description"]
		del item["menus_appeared"]
		del item["times_appeared"]
		del item["first_appeared"]
		del item["last_appeared"]
		item["type"] = "food"
		results.append(item)

	beers = csv.parse_file(fpath_beers, beers_count, 0.25)
	for beer in beers:
		del beer["idx"]
		del beer["abv"]
		del beer["ibu"]
		del beer["id"]
		del beer["style"]
		del beer["ounces"]
		beer["manu"] = csv.retreive(fpath_brew, int(beer["brewery_id"])-1)["name"]
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
# it = items(items_raw(20))
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
	for i in range(count):
		result = (rand_pick(drinkers).name, rand_pick(bars).name)
		s.add(result)
	for r in s:
		results.append(Frequent(r[0], r[1]))
	return results

# test
# f = frequents(drinkers(10), bars(10), 20)
# for freq in f:
# 	print(freq.csv())

def likes(drinkers, items, count):
	pass