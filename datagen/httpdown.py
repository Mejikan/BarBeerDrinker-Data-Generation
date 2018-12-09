import requests
import os

fp = "temp.html"

def download(url, parse, del_file=True):
	r = requests.get(url, allow_redirects=True)
	f = open(fp, 'wb')

	try:
		f.write(r.content)
	finally:
		f.close()
	
	with open(fp) as f:
		parse(f)
	
	if del_file:
		os.remove(fp)

