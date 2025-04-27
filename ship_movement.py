import requests
import json
import time

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yMCIsImlhdCI6MTc0NTM3MTEzOSwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YR2svGz8zTThGdfLvpS6nhX9xgqlzuAxM0SnIRT3-JwlPrw8_z-IcGdxffRXqOVfE4Tf4RKPMLsX0bMzERVJBBkYNLy_cngKAnGTb3xWnPv4GE93jupZSjRmzmt1dXvLnMP6vRaCiO2qP-tHuiBm8gfk3IDyJ9MwRFz-58cJFSYtyFTaDz-FL_fQXRN4kcOPZMTbu-TaSZK-m68TSevr4eIfywyYm31aA7kxYbNxDCXm8EXQJi3g1n8mHfGh9CTPFFBJpdWz7jxqE1p20gqjqVfBSxALCvosjLb4KmsORItv_sCTwVDl2sdYWUbGvxbQNYqphusPTttQ1hfJ_l1fAXnGmlTa0ksQhMx9Eh4rnA8WBU4rL_P6wx05_CkdR7-910CA-l7Kav4wc0R6wM1f50xIYJeN481zkiddoj3T1IhOcDKo3AmkkUlqOjVHlDrBabIkQPvbvRvLrg_bZdIixNEPIa9AliainDoY7dwmu6Q0MAdSaqewIundzfZLDOJGOeSDdw_MPRNGW9ioGxzKgxZaJ4VhjMM5HIfMXDd_z1UY57PugnnUUXEgcPRan_HjCXHSil-xvfy4K2rcrGMu96SFfBCd4U_Jc8mL00yyAJ_bvoenJgpxRFy0V8bQd6lHoyOpj7YrM9yejkYQsMMnT2Fthd8suxj5MdLJw3PuBlE'
header = 'Authorization: Bearer ' + token
headers = {'Authorization': 'Bearer ' + token}
symbol = 'LONESTARTIGER'
faction = 'DOMINION'
url = 'https://api.spacetraders.io/v2/'
systemSymbol = 'X1-MU86'
location_type = 'ENGINEERED_ASTEROID'
destination = 'X1-MU86-ZZ5F'
ship_symbol = 'LONESTARTIGER-1'
#should change ship cooldown to lookup for ship and be dynamic rather than hardcoded
ship_cooldown = 80

#this returns the data about the engineered asteroid in the system
engineered_asteroid = requests.get('https://api.spacetraders.io/v2/systems/' +systemSymbol + '/waypoints?type=' + location_type, headers=headers)
#print(engineered_asteroid.text)
engineered_asteroid_pretty = json.loads(engineered_asteroid.text)
print(json.dumps(engineered_asteroid_pretty, indent=4))

#navigate to waypoint
navigate = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/navigate', headers=headers, data={'waypointSymbol': destination})
navigate_pretty = json.loads(navigate.text)
print(json.dumps(navigate_pretty, indent=4))

#dock at waypoint to the refuel
dock = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/dock', headers=headers, data={'waypointSymbol': destination})
dock_pretty = json.loads(dock.text)
print(json.dumps(dock_pretty, indent=4))

#refuel, only succeeds if location has fuel for sale, 1 unit at market replenishes 100 units in ship tank; will get error if try to refuel at a location that doesn't have fuel
fuel = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/refuel', headers=headers)
fuel_pretty = json.loads(fuel.text)
print(json.dumps(fuel_pretty, indent=4))

#go into orbit after refueling to prep for mining
orbit = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/orbit', headers=headers)
orbit_pretty = json.loads(orbit.text)
print(json.dumps(orbit_pretty, indent=4))

#begin mining
mine = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/extract', headers=headers)
mine_pretty = json.loads(mine.text)
print(json.dumps(mine_pretty, indent=4))

## you can jettison non-contract cargo, but I don't know how to do that yet, so this will be commented out
#jettison = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/jettison', headers='Content-Type: application/json', data={'symbol': '', 'units': ''})
#jettison_pretty = json.loads(jettison.text)
#print(json.dumps(jettison_pretty, indent=4))

#check cargo hold post mining
cargo = requests.get('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/cargo', headers=headers)
cargo_pretty = json.loads(cargo.text)
print(json.dumps(cargo_pretty, indent=4))

mining_attempts = 1
while True:
    #perform mining
    mine = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/extract', headers=headers)
    mine_pretty = json.loads(mine.text)
    print(json.dumps(mine_pretty, indent=4))

    #check cargo hold post mining
    cargo = requests.get('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/cargo', headers=headers)
    cargo_pretty = json.loads(cargo.text)
    print(json.dumps(cargo_pretty, indent=4))
    cargo_units = cargo_pretty.get("data").get("capacity")
    cargo_units_used = cargo_pretty.get("data").get("units")
    print(f"Cargo Units: {cargo_units}\n"
          f"Cargo Units Used: {cargo_units_used}\n"
          #ToDo Pretty Print Inventory
          f"Inventory: {cargo_pretty.get('data').get('inventory')}\n")
    if cargo_units_used >= cargo_units:
        print("Cargo hold is full, stopping mining.")
        break
    print(f"Mining attempt {mining_attempts}\n")
    mining_attempts += 1
    time.sleep(ship_cooldown)