import requests
import json
req = requests.get("https://api.github.com/users/zero9495/repos")
data = req.json()

with open('repos.json', 'w') as file:
    json.dump(data, file)