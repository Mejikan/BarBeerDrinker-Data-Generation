import random

drinkers = ["Joe", "Ann", "Rohit", "Chris", "Brett"]
beers = ["Bud", "Fat Tire", "Heineken", "Coors", "Corona", "Sam Adams"]

# picks randomly from a list
def rand_pick(lst):
	return lst[random.randrange(0, len(lst))]

N = 20
likes = []
for i in range(N):
	t = (rand_pick(drinkers), rand_pick(beers))
	while t in likes:
		t = (rand_pick(drinkers), rand_pick(beers))
	likes.append(t)

print(likes)
