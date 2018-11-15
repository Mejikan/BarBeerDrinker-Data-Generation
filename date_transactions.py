import random as rand
import datetime as dt

def day_of_week_match(date, day_of_week):
	d_day_of_week = int(date.strftime("%w"))+1
	return d_day_of_week == day_of_week

def rand_date(day_of_week):
	# add popular dates for Jan 1 and July 4
	lottery = rand.randint(1, 10)
	if lottery == 1:
		d = dt.datetime(2016, 1, 1)
		if day_of_week_match(d, day_of_week):
			return d
		d = dt.datetime(2017, 1, 1)
		if day_of_week_match(d, day_of_week):
			return d
	elif lottery == 2:
		d = dt.datetime(2016, 7, 4)
		if day_of_week_match(d, day_of_week):
			return d
		d = dt.datetime(2017, 7, 4)
		if day_of_week_match(d, day_of_week):
			return d

	while True:
		try:
			year = rand.randint(2016, 2017)
			month = rand.randint(1, 12)
			day_of_month = rand.randint(1, 31)
			d = dt.datetime(year, month, day_of_month)
			if day_of_week_match(d, day_of_week):
				return d
		except:
			pass
