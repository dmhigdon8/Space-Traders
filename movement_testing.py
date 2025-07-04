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
contract_id = gt.see_contracts()[0]['id']
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
ship1.mine(contract_item)

# 9. Travel to the delivery location
ship1.navigate_to_waypoint(contract_delivery_location)
print(ship1.get_ship_status())
print(ship1.get_ship_location())
config.dock_ship(ship1.symbol)

# 10. Deliver the item
    # check cargo to see if we have enough of the item
cargo = requests.get('https://api.spacetraders.io/v2/my/ships/' + ship1.symbol + '/cargo', headers=config.headers)
cargo_pretty = json.loads(cargo.text)
print(json.dumps(cargo_pretty, indent=4)) 

cargo_quantity = cargo_pretty['data']['inventory'][0]['units'] if cargo_pretty['data']['inventory'][0]['symbol'] == contract_item else 0
print(f"Cargo quantity of {contract_item}: {cargo_quantity}")

    #deliver contract goods
contract_delivery = requests.post('https://api.spacetraders.io/v2/my/contracts/' + contract_id + '/deliver', headers=config.headers, json={"shipSymbol": "LONESTARTIGER-1","tradeSymbol": contract_item, "units": cargo_quantity})
contract_delivery_pretty = json.loads(contract_delivery.text)
print(json.dumps(contract_delivery_pretty, indent=4))

# 11. Attempt to refuel the ship
config.refuel_ship(ship1.symbol)

# 12. Back to orbit and back to the asteroid to mine more
config.launch_to_orbit(ship1.symbol)
ship1.navigate_to_waypoint(engineered_asteroid)
