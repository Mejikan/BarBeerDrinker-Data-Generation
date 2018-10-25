import requests

url = "http://www.craftbeernamegenerator.com/"
response = requests.get(url)

print(response.text)

