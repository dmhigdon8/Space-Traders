import config
import requests
import json

response = requests.get(config.url + 'my/ships', headers=config.headers)
ships_data = response.json()
print(json.dumps(ships_data, indent=4))

ships= {}
for index, ship in enumerate(ships_data['data'], start=1):
    ships[f'ship_{index}_symbol'] = ship['symbol']
    ships[f'ship_{index}_system'] = ship['nav']['systemSymbol']
    ships[f'ship_{index}_waypoint'] = ship['nav']['waypointSymbol']


for key, value in ships.items():
    print(f"{key}: {value}") 

print(ships['ship_1_system'])