import httpdown as httpd

def index_of_end(match, search):
	return search.index(match) + len(match)

og = []
rl = []

def og_filtr(f):
	names = []
	prices = []

	for line in f:
		item_name = ""
		if "menuItemId" in line:
			start_i = False
			for c in line:
				if c == '>':
					start_i = True
					continue
				elif start_i and c == '<':
					item_name = item_name.strip()
					if len(item_name) > 0:
						names.append(item_name)
					break

				if start_i:
					item_name += c
		
		elif "dollar-sign" in line:
			idx = index_of_end("$</sup>", line)
			prices.append( float(int(line[idx])) + 0.99 )
	
	for n in range(len(names)):
		og.append((names[n], prices[n]))

def og_down():
	url = "https://www.olivegarden.com/menu-listing/dinner"
	httpd.download(url, og_filtr, False)

	print(og, len(og))

og_down()