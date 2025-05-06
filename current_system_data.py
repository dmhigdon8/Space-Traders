import config
import requests
import json
from ships import ships

systemSymbol = ships['ship_1_system']
print(systemSymbol)
#finalized fuel station function
#TODO: add to config.py? See if I can calculate the distance between the two waypoints (euclidean distance) from ship to waypoints and return nearest to ship
def get_fuel_stations(systemsymbol):
    """
    Gets all of the available places to refuel in the system.
    To do this, it first goes though all of the market places and checks if they have fuel as a trade good.
    Then it goes through all of the fuel stations and adds them to the list.
    Finally, it combines the two lists and returns them.
    """
    #begin by getting marketplaces with fuel as a trade good
    response = requests.get(config.url + 'systems/' + systemSymbol + '/waypoints', headers=config.headers)
    #print(response.text)
    json_data = response.json()
    waypoints = json_data.get("data", [])
    #print(json.dumps(waypoints, indent=4))

    fuel_marketplaces = []
    for waypoint in waypoints:
        for trait in waypoint.get("traits", []):       
            if trait.get("symbol") == "MARKETPLACE":
                trade_goods_response = requests.get(f'https://api.spacetraders.io/v2/systems/{systemSymbol}/waypoints/{waypoint.get("symbol")}/market', headers=config.headers)
                trade_goods_json = trade_goods_response.json()
                trade_goods = trade_goods_json.get("data", {}).get("exchange", [])
                for trade_good in trade_goods:
                    if trade_good['symbol'] == "FUEL":
                        fuel_waypoint_data = {
                            "symbol": waypoint.get("symbol"),
                            "x": waypoint.get("x"),
                            "y": waypoint.get("y"),
                            "type": "MARKETPLACE"
                        }
                        fuel_marketplaces.append(fuel_waypoint_data)

    #then get all fuel stations
    response = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + 'FUEL_STATION', headers=config.headers)
    json_data = response.json()
    fuel_stations = json_data.get("data", [])

    fuel_station_list = []
    for fuel_station in fuel_stations:
        fuel_station_data = {
            "symbol": fuel_station.get("symbol"),
            "x": fuel_station.get("x"),
            "y": fuel_station.get("y"),
            "type": "FUEL_STATION"
        }
        fuel_station_list.append(fuel_station_data)

    
    combined_fuel_station_dict = {}
    for fuel_station in fuel_marketplaces:
        combined_fuel_station_dict[fuel_station['symbol']] = fuel_station
    for fuel_station in fuel_station_list:
        if fuel_station['symbol'] not in combined_fuel_station_dict:
            combined_fuel_station_dict[fuel_station['symbol']] = fuel_station
    all_system_fuel_stations = list(combined_fuel_station_dict.values())
    return all_system_fuel_stations

#call the function to get all fuel stations in the system
all_system_fuel_stations = get_fuel_stations(systemSymbol)
print(all_system_fuel_stations)

#get all waypoints in current system
## Ex: X1-DF55-A1; X1 is the sector, DF55 is the system, A1 is the station
#by default, uses the system of the first ship from ships.py
response = requests.get(config.url + 'systems/' + systemSymbol + '/waypoints', headers=config.headers)
print(response.text)
json_data = response.json()
waypoints = json_data.get("data", [])
print(json.dumps(waypoints, indent=4))

#find the types of waypoints in the system
waypoint_types = []
for waypoint in waypoints:
    if waypoint.get("type") not in waypoint_types:
        waypoint_types.append(waypoint.get("type"))

print(f"Waypoint Types: {waypoint_types}\n")

#find the waypoint symbols in the system with a market
response = requests.get(config.url + 'systems/' + systemSymbol + '/waypoints', headers=config.headers)
json_data = response.json()
traits = json_data.get("data", [])
for trait in traits['traits']['symbol']:
    print(trait['symbol'])

# response is a class 'requests.models.Response'
response = requests.get(config.url + 'systems/' + systemSymbol + '/waypoints', headers=config.headers)
print(type(response))
#json_data is a dict
json_data = response.json()
print(type(json_data))
#waypoints is a list of dicts
waypoints = json_data.get("data", [])
print(type(waypoints))


#define function to get trade goods for a waypoint
def get_trade_goods(waypoint_symbol):
    response = requests.get(f'https://api.spacetraders.io/v2/systems/{systemSymbol}/waypoints/{waypoint_symbol}/market', headers=config.headers)
    if response.status_code == 200:
        trade_goods = response.json().get("data", {}).get("tradeGoods", [])
        return trade_goods
    else:
        print(f"Error: {response.status_code}")
        return None
    
get_trade_goods('X1-KG25-A1')
#1: X1-KG25-A1; 13, -20
#2: X1-KG25-FA5C; 26, 11
#3: X1-KG25-B6; 96, -163
#4: X1-KG25-B7; 200, -278
response = requests.get(f'https://api.spacetraders.io/v2/systems/{systemSymbol}/waypoints/X1-KG25-A1/market', headers=config.headers)
json_data = response.json()
goods = json_data.get("data", {}).get("exchange")
for good in goods:
    print(good['symbol'])



#proof of concept
#loop through marketplaces in current system and return those that list fuel as a trade good
#then loop through fuel station types
#look at all waypoints in the system
response = requests.get(config.url + 'systems/' + systemSymbol + '/waypoints', headers=config.headers)
print(response.text)
json_data = response.json()
waypoints = json_data.get("data", [])
print(json.dumps(waypoints, indent=4))

fuel_marketplaces = []
for waypoint in waypoints:
    for trait in waypoint.get("traits", []):       
        if trait.get("symbol") == "MARKETPLACE":
            trade_goods_response = requests.get(f'https://api.spacetraders.io/v2/systems/{systemSymbol}/waypoints/{waypoint.get("symbol")}/market', headers=config.headers)
            trade_goods_json = trade_goods_response.json()
            trade_goods = trade_goods_json.get("data", {}).get("exchange", [])
            for trade_good in trade_goods:
                if trade_good['symbol'] == "FUEL":
                    fuel_waypoint_data = {
                        "symbol": waypoint.get("symbol"),
                        "x": waypoint.get("x"),
                        "y": waypoint.get("y"),
                        "type": "MARKETPLACE"
                    }
                    fuel_marketplaces.append(fuel_waypoint_data)

for item in fuel_marketplaces:
    print(item)

#### 2nd half of proof of concept, fuel stations
response = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + 'FUEL_STATION', headers=config.headers)
json_data = response.json()
fuel_stations = json_data.get("data", [])

fuel_station_list = []
for fuel_station in fuel_stations:
    fuel_station_data = {
        "symbol": fuel_station.get("symbol"),
        "x": fuel_station.get("x"),
        "y": fuel_station.get("y"),
        "type": "FUEL_STATION"
    }
    fuel_station_list.append(fuel_station_data)

for item in fuel_station_list:
    print(item)


                    #print(str(iterator) + ": " + str(waypoint.get("symbol")) + "; " + str(waypoint.get("x")) + ", " + str(waypoint.get("y")))
                    #iterator += 1
            #print(str(iterator) + ": " + str(waypoint.get("symbol")) + "; " + str(waypoint.get("x")) + ", " + str(waypoint.get("y")))
            #iterator += 1




print(combined_fuel_station_dict)

for fuel_station in fuel_marketplaces:
    if fuel_station not in all_system_fuel_stations:
        all_system_fuel_stations.append(fuel_station)
for fuel_station in fuel_station_list:
    if fuel_station['symbol'] not in all_system_fuel_stations:
        all_system_fuel_stations.append(fuel_station)

print(all_system_fuel_stations)

response = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + 'FUEL_STATION', headers=config.headers)
print(json.dumps(response.json(), indent=4))
#trade_goods = [good['symbol'] for good in response.json()['data']['tradeGoods']]
#print(trade_goods)

waypoints_with_market = []
iterator = 1
for waypoint in waypoints:
    for trait in waypoint.get("traits", []):       
        if trait.get("symbol") == "MARKETPLACE":
            print(str(iterator) + ": " + str(waypoint.get("symbol")) + "; " + str(waypoint.get("x")) + ", " + str(waypoint.get("y\n")))
            iterator += 1
                                     
print(f"Waypoints with Market: {waypoints_with_market}\n")



####
response = requests.get(f'https://api.spacetraders.io/v2/systems/{nav['systemSymbol']}/waypoints/X1-KG25-B7', headers=config.headers)
print(json.dumps(response.json(), indent=4))
traits = [trait['symbol'] for trait in response.json()['data']['traits']]
####

#reference of how to get trade goods
response = requests.get(f'https://api.spacetraders.io/v2/systems/{nav['systemSymbol']}/waypoints/X1-KG25-B7/market', headers=config.headers)
print(json.dumps(response.json(), indent=4))
trade_goods = [good['symbol'] for good in response.json()['data']['tradeGoods']]
print(trade_goods)




if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()

    # Extract the data from the JSON response
    waypoints = json_data.get("data", [])
    waypoint_count = 1

    for waypoint in waypoints:
        waypoint_symbol = waypoint.get("symbol")
        waypoint_type = waypoint.get("type")
        waypoint_x = waypoint.get("x")
        waypoint_y = waypoint.get("y")
        waypoint_coordinates = (waypoint_x, waypoint_y)

        #Begin Orbitals
        orbitals = waypoint.get("orbitals")
        orbital_symbol_list = []
        for item in orbitals:
            orbital_symbol_list.append(item.get("symbol"))
        orbital_amount = len(orbitals)
        print(f"~~~Begin Waypoint {waypoint_count}~~~  \n"
              f"--------About--------\n"
              f"Symbol: {waypoint_symbol} \n"
              f"Type: {waypoint_type} \n"
              f"Coordinates: {waypoint_coordinates}\n"
              f"Orbital Amount: {orbital_amount}")
        if len(orbital_symbol_list) > 0:
              print(f"Orbital List: {orbital_symbol_list}\n")
        
        #Begin Traits
        print("---Traits---\n")
        traits = waypoint.get("traits", [])
        trait_counter = 1
        for trait in traits:
            trait_symbol = trait.get("symbol")
            trait_name = trait.get("name")
            trait_description = trait.get("description")

            print(f"    ---->Begin Trait {trait_counter}\n"
                  f"    Symbol: {trait_symbol} \n"
                  f"    Name: {trait_name}\n"
                  f"    Description: {trait_description}\n"
                  f"    ----<End Trait {trait_counter} \n")
            trait_counter += 1
        print(f"---End Traits---\n")

        print(f"~~~End Waypoint {waypoint_count}~~~\n") 
        waypoint_count += 1
    
else:
    print(f"Error: {response.status_code}")
    print(response.text)

