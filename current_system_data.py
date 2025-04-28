import config
import requests
import json
from ships import ships

systemSymbol = ships['ship_1_system']

#get all waypoints in current system
## Ex: X1-DF55-A1; X1 is the sector, DF55 is the system, A1 is the station
#by default, uses the system of the first ship from ships.py
response = requests.get(config.url + 'systems/' + systemSymbol + '/waypoints', headers=config.headers)
print(response.text)

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