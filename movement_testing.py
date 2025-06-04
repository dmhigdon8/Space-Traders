import config
import requests
import json
import time


#STEPS# 1. Create a ship instance with the symbol 'LONESTARTIGER-1'.
gt = config.User()

# 2. Print the ship's details.
ship1 = config.Ship('LONESTARTIGER-1')
print(ship1.fuel_percentage)

# 3. Check contracts and accept
gt.see_contracts()
gt.accept_first_contract()

# 4. Store item the contract is for
contract_item = gt.see_contracts()[0]['terms']['deliver'][0]['tradeSymbol']
contract_quantity = gt.see_contracts()[0]['terms']['deliver'][0]['unitsRequired']
contract_delivery_location = gt.see_contracts()[0]['terms']['deliver'][0]['destinationSymbol'] 
print(f"Contract item: {contract_item}, Quantity: {contract_quantity}, Delivery Location: {contract_delivery_location}")


# 5. Find item/asteroid to mine for the item
location_type = 'ENGINEERED_ASTEROID'
systemSymbol = ship1.system
engineered_asteroid = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + location_type, headers=config.headers).json()['data'][0]['symbol']

# 6. Undock and travel to the asteroid
config.launch_to_orbit(ship1.symbol)

# 7. Travel to the asteroid
ship1.navigate_to_waypoint(engineered_asteroid)
print(ship1.get_ship_status())
print(ship1.get_ship_location())

# 8. Mine the asteroid for the item
# need to fix this, it's not working, also should add in logic to navigate to sell/deliver items once cargo is full
#test
ship1.mine(contract_item)
