import requests
import json
req = requests.get("https://api.openweathermap.org/data/2.5/weather?q=London&appid=40e0a1c154730d010f92e1cd91bcad2f")
data = req.json()

with open('london.json', 'w') as file:
    json.dump(data, file)