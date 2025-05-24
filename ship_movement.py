# This file contains logic to move the ship to a location, refuel, and mine

# MODULES
import config
import requests
import json
import time
from ships import ships

# VARIABLES
#manually defined variables
location_type = 'ENGINEERED_ASTEROID'
ship_cooldown = 80

#pulls from ships.py, loops through all ships and saves variables for each
#be aware of using ship variables from ships.py vs config.py
systemSymbol = ships['ship_1_system']
ship_symbol = ships['ship_1_symbol']

#calls functions for agent and ship info defined in config.py
#calling ship & agent functions from config to get ship and agent info
ship_symbol, ship_status, ship_flight_mode, ship_system, ship_waypoint, ship_cargo_capacity, ship_cargo_used, ship_cargo_free, ship_fuel_capacity, ship_fuel_available, ship_fuel_burned = config.get_ship_info('LONESTARTIGER-1') 
account_id, account_symbol, headquarters, credits, faction, ship_count = config.get_agent_info()

#SCRATCH
print(f"Ship Symbol: {ship_symbol}\n"
      f"Status: {ship_status}\n"
      f"Fuel Capacity: {ship_fuel_capacity}\n"
      f"Fuel Available: {ship_fuel_available}\n")

# FUNCTIONS
   # begin with need to refuel logic

def get_fuel():
    """
    This function checks the ship status, if in orbit, it docks and refuels, otherwise just refuels.
    """



#situations to check
# 1. need fuel and docked
# 2. need fuel and in orbit
# 3. full fuel and docked
#---first 3 should all end in "full fuel and in orbit"
# 4. check for a status that isn't docked or orbit
# 5. navigate to destination

#1
if config.get_ship_info("LONESTARTIGER-1")['ship_fuel_capacity'] > config.get_ship_info("LONESTARTIGER-1")['ship_fuel_available'] and config.get_ship_info("LONESTARTIGER-1")['ship_status'] == 'DOCKED': #replace with ship argument
    print("Ship is docked and needs fuel. Attempting to refuel.\n")
    # refueling ship
    config.refuel_ship('LONESTARTIGER-1') #replace with ship argument

    # back to orbit for travel
    config.launch_to_orbit('LONESTARTIGER-1') #replace with ship argument

#2
elif config.get_ship_info("LONESTARTIGER-1")['ship_fuel_capacity'] > config.get_ship_info("LONESTARTIGER-1")['ship_fuel_available'] and config.get_ship_info("LONESTARTIGER-1")['ship_status'] != 'DOCKED': #replace with ship argument
#    use nearest fuel function to get that waypoint, travel to waypoint, then go through fueling process
    config.dock_ship('LONESTARTIGER-1', config.find_nearest_fuel_station('LONESTARTIGER-1')['symbol']) #replace with ship argument

    # back to orbit for travel
    config.launch_to_orbit('LONESTARTIGER-1') #replace with ship argument

#3
elif config.get_ship_info("LONESTARTIGER-1")['ship_fuel_capacity'] == config.get_ship_info("LONESTARTIGER-1")['ship_fuel_available'] and config.get_ship_info("LONESTARTIGER-1")['ship_status'] == 'DOCKED': #replace with ship argument
    print("Ship is docked and has full fuel, no need to refuel. Going to orbit.\n")
    config.launch_to_orbit('LONESTARTIGER-1') #replace with ship argument

#4
elif config.get_ship_info("LONESTARTIGER-1")['ship_status'] not in ('DOCKED','IN_ORBIT'): #replace with ship argument
    print("Ship is not docked or in orbit, attempting to navigate to nearest waypoint.\n")

#5 next a series of functions that define goal
    # example, if contract, function that gets contract deliverable, finds location, and navigates to that location, mines, jettisons non contract items, and returns to the market
    # if mining for money and not contract, function that finds nearest resource,  mines, and returns to the market

else config.get_ship_info("LONESTARTIGER-1")['ship_fuel_capacity'] == config.get_ship_info("LONESTARTIGER-1")['ship_fuel_available'] and config.get_ship_info("LONESTARTIGER-1")['ship_status'] != 'DOCKED': #replace with ship argument






#need to finish this
def ship_navigation(ship_symbol, destination):
    #check fuel
    fuel = requests.get(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}/fuel', headers=config.headers)
    fuel_pretty = json.loads(fuel.text)
    print(json.dumps(fuel_pretty, indent=4))
    
    # Check if the ship is docked
    response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}', headers=config.headers)
    ship_data = response.json()
    print(json.dumps(ship_data, indent=4))
    ship_status = ship_data.get("data").get("nav").get("status")
    print(f"Ship Status: {ship_status}")
    
    if ship_status == "DOCKED":
        # If docked, go to orbit
        orbit = requests.post(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}/orbit', headers=config.headers)
        orbit_pretty = json.loads(orbit.text)
        print(json.dumps(orbit_pretty, indent=4))
    
    # Navigate to the destination waypoint
    navigate = requests.post(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}/navigate', headers=config.headers, data={'waypointSymbol': destination})
    navigate_pretty = json.loads(navigate.text)
    print(json.dumps(navigate_pretty, indent=4))
    return navigate_pretty



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

dock = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/dock', headers=config.headers, data={'waypointSymbol': ship_waypoint})
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

test_dock = dock_pretty['data']['nav']['status']
print(test_dock)
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

ship_symbol = 'LONESTARTIGER-1'
destination = 'X1-KG25-B13'

def ship_navigation(ship_symbol, destination):
    # Check if the ship is docked
    response = requests.get(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}', headers=config.headers)
    ship_data = response.json()
    print(json.dumps(ship_data, indent=4))
    ship_status = ship_data.get("data").get("nav").get("status")
    print(f"Ship Status: {ship_status}")
    
    if ship_status == "DOCKED":
        # If docked, go to orbit
        orbit = requests.post(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}/orbit', headers=config.headers)
        orbit_pretty = json.loads(orbit.text)
        print(json.dumps(orbit_pretty, indent=4))
    
    # Navigate to the destination waypoint
    navigate = requests.post(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}/navigate', headers=config.headers, data={'waypointSymbol': destination})
    navigate_pretty = json.loads(navigate.text)
    print(json.dumps(navigate_pretty, indent=4))
    return navigate_pretty

    #add in code that saves arrival time as a variable and prints how long until arrival every 30 seconds
    #then print arrived
    #begin mining
    #need to functionalize the mining



# Call the function with the ship symbol and destination
ship_navigation(ship_symbol, destination)

navigate = requests.post(f'https://api.spacetraders.io/v2/my/ships/{ship_symbol}/navigate', headers=config.headers, data={'waypointSymbol': destination})
navigate_pretty = json.loads(navigate.text)
print(json.dumps(navigate_pretty, indent=4))

#mining logic
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
    #for item in cargo_pretty['data']['inventory']:
        #NEED TO GENERALIZE THIS, SHOULD PASS A PARAMETER FOR THE ITEM FOR CONTRACT RATHER THAN HARD CODING
        #add parameter for contract run, if contract, jettison non contract items, else keep all until full
    #    if item['symbol'] != 'COPPER_ORE':
    #        jettison_symbol = item['symbol']
    #        jettison_units = item['units']
    #        print(f"Jettisoning {jettison_units} units of {jettison_symbol}")
    #        jettison = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/jettison', headers=config.headers, json={'symbol': jettison_symbol, 'units': jettison_units})
  
    if cargo_units_used >= cargo_units:
        print("Cargo hold is full, stopping mining.")
        break
    print(f"Mining attempt {mining_attempts}\n")
    mining_attempts += 1
    time.sleep(ship_cooldown)


