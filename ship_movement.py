import config
import requests
import json
import time
from ships import ships

#token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yMCIsImlhdCI6MTc0NTM3MTEzOSwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YR2svGz8zTThGdfLvpS6nhX9xgqlzuAxM0SnIRT3-JwlPrw8_z-IcGdxffRXqOVfE4Tf4RKPMLsX0bMzERVJBBkYNLy_cngKAnGTb3xWnPv4GE93jupZSjRmzmt1dXvLnMP6vRaCiO2qP-tHuiBm8gfk3IDyJ9MwRFz-58cJFSYtyFTaDz-FL_fQXRN4kcOPZMTbu-TaSZK-m68TSevr4eIfywyYm31aA7kxYbNxDCXm8EXQJi3g1n8mHfGh9CTPFFBJpdWz7jxqE1p20gqjqVfBSxALCvosjLb4KmsORItv_sCTwVDl2sdYWUbGvxbQNYqphusPTttQ1hfJ_l1fAXnGmlTa0ksQhMx9Eh4rnA8WBU4rL_P6wx05_CkdR7-910CA-l7Kav4wc0R6wM1f50xIYJeN481zkiddoj3T1IhOcDKo3AmkkUlqOjVHlDrBabIkQPvbvRvLrg_bZdIixNEPIa9AliainDoY7dwmu6Q0MAdSaqewIundzfZLDOJGOeSDdw_MPRNGW9ioGxzKgxZaJ4VhjMM5HIfMXDd_z1UY57PugnnUUXEgcPRan_HjCXHSil-xvfy4K2rcrGMu96SFfBCd4U_Jc8mL00yyAJ_bvoenJgpxRFy0V8bQd6lHoyOpj7YrM9yejkYQsMMnT2Fthd8suxj5MdLJw3PuBlE'
#header = 'Authorization: Bearer ' + token
#headers = {'Authorization': 'Bearer ' + token}
#symbol = 'LONESTARTIGER'
#faction = 'DOMINION'
#url = 'https://api.spacetraders.io/v2/'
#systemSymbol = 'X1-MU86'
systemSymbol = ships['ship_1_system']
ship_symbol = ships['ship_1_symbol']
location_type = 'ENGINEERED_ASTEROID'
ship_cooldown = 80

# get waypoint for engineered asteroid
engineered_asteroid = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + location_type, headers=config.headers)
#print(engineered_asteroid.text)
engineered_asteroid_data = engineered_asteroid.json()
print(json.dumps(engineered_asteroid_data, indent=4))
destination = engineered_asteroid_data.get("data")[0].get("symbol")
print(f"Destination: {destination}")


#navigate to waypoint
navigate = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/navigate', headers=config.headers, data={'waypointSymbol': destination})
navigate_pretty = json.loads(navigate.text)
print(json.dumps(navigate_pretty, indent=4))

#dock at waypoint to the refuel
dock = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/dock', headers=config.headers, data={'waypointSymbol': destination})
dock_pretty = json.loads(dock.text)
print(json.dumps(dock_pretty, indent=4))

#refuel, only succeeds if location has fuel for sale, 1 unit at market replenishes 100 units in ship tank; will get error if try to refuel at a location that doesn't have fuel
fuel = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/refuel', headers=config.headers)
fuel_pretty = json.loads(fuel.text)
print(json.dumps(fuel_pretty, indent=4))

#go into orbit after refueling to prep for mining
orbit = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/orbit', headers=config.headers)
orbit_pretty = json.loads(orbit.text)
print(json.dumps(orbit_pretty, indent=4))

#begin mining
mine = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/extract', headers=config.headers)
mine_pretty = json.loads(mine.text)
print(json.dumps(mine_pretty, indent=4))

## you can jettison non-contract cargo, but I don't know how to do that yet, so this will be commented out
#jettison = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/jettison', headers='Content-Type: application/json', data={'symbol': '', 'units': ''})
#jettison_pretty = json.loads(jettison.text)
#print(json.dumps(jettison_pretty, indent=4))

#check cargo hold post mining
cargo = requests.get('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/cargo', headers=config.headers)
cargo_pretty = json.loads(cargo.text)
print(json.dumps(cargo_pretty, indent=4))

mining_attempts = 1
while True:
    #perform mining
    mine = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/extract', headers=config.headers)
    mine_pretty = json.loads(mine.text)
    print(json.dumps(mine_pretty, indent=4))

    #check cargo hold post mining
    cargo = requests.get('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/cargo', headers=config.headers)
    cargo_pretty = json.loads(cargo.text)
    print(json.dumps(cargo_pretty, indent=4))
    cargo_units = cargo_pretty.get("data").get("capacity")
    cargo_units_used = cargo_pretty.get("data").get("units")
    print(f"Cargo Units: {cargo_units}\n"
          f"Cargo Units Used: {cargo_units_used}\n"
          #ToDo Pretty Print Inventory
          f"Inventory: {cargo_pretty.get('data').get('inventory')}\n")
    for item in cargo_pretty['data']['inventory']:
        #NEED TO GENERALIZE THIS, SHOULD PASS A PARAMETER FOR THE ITEM FOR CONTRACT RATHER THAN HARD CODING
        if item['symbol'] != 'COPPER_ORE':
            jettison_symbol = item['symbol']
            jettison_units = item['units']
            print(f"Jettisoning {jettison_units} units of {jettison_symbol}")
            jettison = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/jettison', headers=config.headers, json={'symbol': jettison_symbol, 'units': jettison_units})
  
    if cargo_units_used >= cargo_units:
        print("Cargo hold is full, stopping mining.")
        break
    print(f"Mining attempt {mining_attempts}\n")
    mining_attempts += 1
    time.sleep(ship_cooldown)

    #have 16 of copper_ore
    #have 39

    #need 49

cargo = requests.get('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/cargo', headers=config.headers)
cargo_pretty = json.loads(cargo.text)
print(json.dumps(cargo_pretty, indent=4))
for item in cargo_pretty['data']['inventory']:
    print(item['symbol'])


jettison = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/jettison', headers=config.headers, json={'symbol': 'ICE_WATER', 'units': 9})
jettison_pretty = json.loads(jettison.text)
print(json.dumps(jettison_pretty, indent=4))


#only sell fuel, go to orbit to go to new market
orbit = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/orbit', headers=config.headers)
orbit_pretty = json.loads(orbit.text)
print(json.dumps(orbit_pretty, indent=4))

#NAVIGATE to planet with market
#engineered_asteroid is 'X1-KG25-FA5C'
navigate = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/navigate', headers=config.headers, data={'waypointSymbol': 'X1-KG25-H53'})
navigate_pretty = json.loads(navigate.text)
print(json.dumps(navigate_pretty, indent=4))

#dock at waypoint
dock = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/dock', headers=config.headers, data={'waypointSymbol': 'X1-KG25-H53'})
dock_pretty = json.loads(dock.text)
print(json.dumps(dock_pretty, indent=4))

#see if market and if sell
waypoint = nav['waypointSymbol']
response = requests.get(f'https://api.spacetraders.io/v2/systems/{nav['systemSymbol']}/waypoints/X1-KG25-B7', headers=config.headers)
print(json.dumps(response.json(), indent=4))
traits = [trait['symbol'] for trait in response.json()['data']['traits']]
print('MARKETPLACE' in traits)  # Must be True

response = requests.get(f'https://api.spacetraders.io/v2/systems/{nav['systemSymbol']}/waypoints/X1-KG25-B7/market', headers=config.headers)
print(json.dumps(response.json(), indent=4))
trade_goods = [good['symbol'] for good in response.json()['data']['tradeGoods']]
print(trade_goods)

sell = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/sell', headers=config.headers, json={"symbol": "ALUMINUM_ORE", "units": 3}, )
sell_pretty = json.loads(sell.text)
print(json.dumps(sell_pretty, indent=4))    

#deliver contract goods
contract_delivery = requests.post('https://api.spacetraders.io/v2/my/contracts/cma05flqr9egave72454uphv8/deliver', headers=config.headers, json={"shipSymbol": "LONESTARTIGER-1","tradeSymbol": "COPPER_ORE", "units": 5})
contract_delivery_pretty = json.loads(contract_delivery.text)
print(json.dumps(contract_delivery_pretty, indent=4))

#close contract, receive payment
contract_fulfillment = requests.post('https://api.spacetraders.io/v2/my/contracts/cma05flqr9egave72454uphv8/fulfill', headers=config.headers)
contract_fulfillment_pretty = json.loads(contract_fulfillment.text)
print(json.dumps(contract_fulfillment_pretty, indent=4))


#check contract status
#delivered 39 of 49

#CREDITS
#176,809
#refueled: 176,521
#refueled again: 176,233
#refueled again: 176,089


#STEPS
#1. If docked, go to orbit
#2. If not docked, navigate to waypoint

#contract destination
# 'X1-KG25-H53'

#need to functionize this