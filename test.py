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



test = '0, "elmo, something", 23, "fire", water'
test2 = '5, 7, hello'


print(test.split('"', 1))
print(test2.split('"', 1))

print(r_split(test))