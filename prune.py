# guarantees no duplicate records

file_path = "data/bars.txt"
file_path_o = "data/bars2.txt"

items = set()
with open(file_path) as file:
	for rec in file:
		rec = rec.strip()
		if (len(rec) > 0):
			items.add(rec)

with open(file_path_o, "w") as file:
	for item in items:
		file.write(item + "\n")
	