import config
import requests
import json


#STEPS# 1. Create a ship instance with the symbol 'LONESTARTIGER-1'.
gt = config.User()
# 2. Print the ship's details.
ship1 = config.Ship('LONESTARTIGER-1')
print(ship1.fuel_percentage)
# 3. Check contracts and accept
gt.see_contracts()
len(gt.see_contracts())
# 4. Store item the contract is for
contract_item = gt.see_contracts()[0]['terms']['deliver'][0]['tradeSymbol']
contract_quantity = gt.see_contracts()[0]['terms']['deliver'][0]['unitsRequired']
contract_delivery_location = gt.see_contracts()[0]['terms']['deliver'][0]['destinationSymbol'] 


# 5. Find item/asteroid to mine for the item
location_type = 'ENGINEERED_ASTEROID'
systemSymbol = ship1.system
engineered_asteroid = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + location_type, headers=config.headers).json()['data'][0]['symbol']
# 6. Undock and travel to the asteroid
config.launch_to_orbit(ship1.symbol)
# 7. Travel to the asteroid
ship1.navigate_to_waypoint(engineered_asteroid)
ship1.get_ship_status()

import requests
token: str = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNS0yNSIsImlhdCI6MTc0ODMxNzc1NCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.ALNy8FaGh6thSV2JiHlJvYl7gf2uIOfu7I4Bh8F076zD-wsYFxPryMEVbtrvYx3C_9XWlHoSZWMoVehm9EePg21WWUS70tUuDigAqcyjtj3mOxt2bFHHPPgdcbDWdSaWMDj5dZHBPRaeugZLy6mNCdQHo33UdeAtgBUdFyEv7poUGLwxIkXG4m-sUaI0i3tp7U96AVXvyXE3pISFESQjF_9vw9GTUueWgFpAAzOTTfTISQsHCB9vf0_izLX15E0ry-80UdP0EJesjlwYwc8vnyKj62WSvLzYHbZWl-OqbAtK-k668SYcCR9fJ3G-oSfhyd_PwlfXNPYldFcc7nFxEnQL7S1LnQEIxefTZ8l6M_HrNQWggmmHbxk0pf7dVqVybtNUCRD0-DrFN3x3ewp0tubkCmbmNZd1w3NloGj-56ogIpNSBuABc7nm6XKzQdSdMYltnEbL12hZvyFf1iHaB9A89owXIaFRLU0YqRqPyEbJhnQ_wj6becpyOWpzg4EkMZi4LnsytA61ZSCEjAiDNoxBJaKCv5La8NUbnABeFUyzSlRWA3KdOkL57uPFtf8_eLlEC2nBxOSxxbP5NH7SJgmBR2hjIpSxhr6jDvHW9ViCt_xpwBN7wHvnFk9ZsiH0YyMbNoeX0zzXLqnAXb-B_i_40mv36G-PFsEqsxId26o'
headers = {'Authorization': 'Bearer ' + token}
response = requests.get(f"https://api.spacetraders.io/v2/my/contracts", headers=headers)
response.raise_for_status()  # Raise an error for bad response
data = response.json().get('data')
first_contract = data[0].get('id')
print(first_contract)  # Adjusted to get 'id' directly
print(type(first_contract))
print(type(data))
print(type(response))
print(data)
print(data.get('id', 'No ID found'))

