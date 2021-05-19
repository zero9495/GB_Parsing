import requests
import json


d = dict()

for i in range(10):
	req = requests.get("https://api.kanye.rest/")
	data = req.json()

	elem = {
		"No": i,
		"Joke": data['quote']
	}

	d[i] = elem


with open('jokes.json', 'w') as file:
    json.dump(d, file)