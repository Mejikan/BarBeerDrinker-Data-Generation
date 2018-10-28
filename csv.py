def m_split(line):
	words = []

	word = ""
	switch_p = False
	ci = 0
	while ci < len(line):
		c = line[ci]
		if c == '"':
			if switch_p:
				words.append(word.strip())
				word = ""
				ci += 1
				switch_p = False
			else:
				switch_p = True
		elif c == ',':
			if switch_p:
				word += c
			else:
				words.append(word.strip())
				word = ""
		else:
			word += c
		ci += 1
	
	words.append(word.strip())
	return words

def parse_file(file_path, max_rec, filtr=None):
	recs = []
	with open(file_path) as file:
		line = file.readline().strip()

		# first line is column names
		col_names = m_split(line)
		for col_name in col_names:
			col_name = col_name.strip()

		while (len(recs) < max_rec):
			line = file.readline().strip()
			if not line: break
			col_vals = m_split(line)
			rec = {}
			for i in range(len(col_names)):
				val = col_vals[i].strip()
				rec[col_names[i]] = val
				# if (len(val) <= 45):
				# else:
				# 	fail = True
				# 	break
			# if (random.random() < rand_thresh):
			# 	fail = True
			if filtr and filtr(rec):
				recs.append(rec)
	return recs

def retreive(file_path, row): # row =1 will retreive the first row below the column header row
	rec = {}
	with open(file_path) as file:
		line = file.readline().strip()

		# first line is column names
		col_names = m_split(line)
		for col_name in col_names:
			col_name = col_name.strip()

		line = ""
		for n in range(row): # row 1 is the first row after the header row
			line = file.readline()

		col_vals = m_split(line)
		for i in range(len(col_names)):
			val = col_vals[i].strip()
			rec[col_names[i]] = val
	return rec



	