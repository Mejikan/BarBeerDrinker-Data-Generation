import random

def parse_file(file_path, max_rec, rand_thresh=0):
	recs = []
	with open(file_path) as file:
		line = file.readline().strip()

		# first line is column names
		col_names = line.split(",")
		for col_name in col_names:
			col_name = col_name.strip()

		while (len(recs) < max_rec):
			line = file.readline().strip()
			if not line: break
			col_vals = line.split(",")
			rec = {}
			fail = False
			for i in range(len(col_names)):
				val = col_vals[i].strip()
				if (len(val) <= 45):
					rec[col_names[i]] = val
				else:
					fail = True
					break
			if (random.random() < rand_thresh):
				fail = True
			if not fail:
				recs.append(rec)
	return recs

def retreive(file_path, row): # row =1 will retreive the first row below the column header row
	rec = {}
	with open(file_path) as file:
		line = file.readline().strip()

		# first line is column names
		col_names = line.split(",")
		for col_name in col_names:
			col_name = col_name.strip()

		line = ""
		for n in range(row): # row 1 is the first row after the header row
			line = file.readline()

		col_vals = line.split(",")
		for i in range(len(col_names)):
			val = col_vals[i].strip()
			rec[col_names[i]] = val
	return rec



	