import csv

class Addr:
	def __init__(self, street = "", city = "", state = "", zip_code = ""):
		self.street = street
		self.city = city
		self.state = state
		self.zip_code = zip_code

	def __str__(self):
		return "( street: {0}, city: {1}, state: {2}, zip_code: {3} )".format(self.street, self.city, self.state, self.zip_code)

def get_addr(file_path, skip = 0):
	results = []

	with open(file_path) as file:
		i = 0
		addr = Addr()
		for line in file:
			if (i >= skip*2):
				line = line.strip()
				if (i%2 == 0):
					addr.street = line
				else:
					split = line.split(",")
					addr.city = split[0].strip()
					# if (len(addr.city) > 45):
					# 	print("****poop", addr.city)
					split = split[1].strip().split()
					addr.state = split[0].strip()
					addr.zip_code = split[1].strip()
					results.append(addr)
					addr = Addr()
			i += 1
	return results

# test
#get_addr("data/addr.txt", 499)

# class Phone():
# 	def __init__(self, num = "(000) 000-0000"):
# 		self.number = num

# 	def __str__(self):
# 		return str(self.number)

def get_phone(file_path, skip = 0):
	results = []

	with open(file_path) as file:
		i = 0
		for line in file:
			if (i >= skip):
				line = line.strip()
				results.append(line)
			i += 1
	return results

# test
# print(get_phone("data/phone.txt", 499))

def get_name(file_path, skip = 0):
	results = []

	with open(file_path) as file:
		i = 0
		for line in file:
			if (i >= skip):
				line = line.strip()
				# if (len(line) > 45):
				# 	print("****poop", line)
				results.append(line)
			i += 1
	return results

# test
# print(get_name("data/drinkers.txt"))

def get_bar(file_path, skip = 0):
	results = []
	
	with open(file_path) as file:
		i = 0
		for line in file:
			if (i >= skip):
				line = line.strip()
				# if (len(line) > 45):
				# 	print("****poop", line)
				results.append(line)
			i += 1
	return results

# test
# print(get_bar("data/bars.txt"))