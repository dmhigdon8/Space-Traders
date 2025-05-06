# This file contains the configuration for the Space Traders API

# MODULES
import json
import requests
import time

# VARIABLES
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNS0wNCIsImlhdCI6MTc0NjQ5NTk5NCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.r796OR0T3cHq56J-YxkUCb4cA_a9rJJsMUUeP0f61LAv86lcoBWQ_OtN2_oRtD1vKDqTkHi9XXl8eqIibjvX08hEKLVmLo_xP0jTrKmMOgkkWXDb5Jrlnj_sU_Atn2PxbLeV_afeHQSOFPYhaKyhDZZl-yfZtEU7FdhfByrqIHYqYGsWQ8sAQ8qNcWT5e6HwIEbgxYIvF5fVsP1-dyvr8XbEUH0Wo7yCslYRU9K8ilxKc-zumojXRbuCDAFApTL-mb2UASbuyRjc5SgMV2CJwA6AEdNwWmxI2Y4L6VAgvnM2C9US-8nkeGjDHo3A2HhTBJmw96-8VxPoaCYRBQ274qAzJRWMi_kU0hpkEez1Kd9eYj69q4NMwbOSnjS01FOXJYOu_AeseNWYzMXVrIB-I9ho8Gbmm6S5l4AvOMuMSHtW-1FzGoFeaGtERR7H5hHIZpvNF_5nH4cRxScmhR-QtrPFA2e_zeN1cqkHBiDt1VZzcXOzGzLiFr9U6ARgNx164grsuWR0Fj57Q8SK_zmK52Z-0dXOwGQLSqDxRe5iIMgHEPzAKSNRU8tXv4ft0RTtp8XiSiWpf6R66WJuWZ6PPuU2Zth0m3jFY9QraBFqDwG8gnNe6EThz2Xjr9LXoiNVsx-Vhf7K7LwoxjoSBsqeWXXPCD5sR3uTobeNFTZwVaE'
headers = {'Authorization': 'Bearer ' + token}
url = 'https://api.spacetraders.io/v2/'

response = requests.get(url + 'my/ships', headers=headers)
ships_data = response.json()
print(json.dumps(ships_data, indent=4))

# FUNCTIONS

#agent & account information
def get_agent_info():
    """
    Gets the agent & account information.
    """
    response = requests.get(url + 'my/agent', headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        account_id = json_data.get("data").get("accountId")
        account_symbol = json_data.get("data").get("symbol")
        headquarters = json_data.get("data").get("headquarters")
        credits = json_data.get("data").get("credits")
        faction = json_data.get("data").get("startingFaction")
        ship_count = json_data.get("data").get("shipCount")
        print(f"Account ID: {account_id}\n"
                      f"Symbol: {account_symbol}\n"
                      f"Headquarters: {headquarters}\n"
                      f"Credits: {credits}\n"
                      f"Faction: {faction}\n"
                      f"Ship Count: {ship_count}\n")
        return account_id, account_symbol, headquarters, credits, faction, ship_count

    else:
        print(f"Error: {response.status_code}")
        print(response.text)

get_agent_info()

#ship information
def get_ship_info(ship):
    """
    Get the ship information.
    """
    if not isinstance(ship, str):
        try:
            ship = str(ship)
        except (ValueError, TypeError):
            print("Invalid ship symbol. Please provide a valid string.")
            return None
    #force the parameter to be uppercase
    ship = ship.upper()   
    response = requests.get(url + 'my/ships/' + ship, headers=headers)
    if response.status_code == 200:
        ships_data = response.json()
        ship_symbol = ships_data['data']['symbol']
        ship_status = ships_data['data']['nav']['status']
        ship_flight_mode = ships_data['data']['nav']['flightMode']
        ship_system = ships_data['data']['nav']['systemSymbol']
        ship_waypoint = ships_data['data']['nav']['waypointSymbol']
        ship_x = ships_data['data']['nav']['route']['destination']['x']
        ship_y = ships_data['data']['nav']['route']['destination']['y']
        ship_coord = (ship_x, ship_y)
        ship_cargo_capacity = ships_data['data']['cargo']['capacity']
        ship_cargo_used = ships_data['data']['cargo']['units']
        ship_cargo_free = ships_data['data']['cargo']['capacity'] - ships_data['data']['cargo']['units']
        ship_fuel_capacity = ships_data['data']['fuel']['capacity']
        ship_fuel_available = ships_data['data']['fuel']['current']
        ship_fuel_burned = ships_data['data']['fuel']['capacity'] - ships_data['data']['fuel']['current']
        print(f"Ship Symbol: {ship_symbol}\n"
                        f"---Current Status---\n"
                      f"Ship Status: {ship_status}\n"
                      f"Ship Flight Mode: {ship_flight_mode}\n"
                        f"---Nav Info---\n"
                      f"Ship System: {ship_system}\n"
                      f"Ship Waypoint: {ship_waypoint}\n"
                      f"Ship Coordinates: {ship_coord}\n"
                      f"Ship X: {ship_x}\n"
                      f"Ship Y: {ship_y}\n"
                        f"---Cargo Info---\n"
                      f"Ship Cargo Capacity: {ship_cargo_capacity}\n"
                      f"Ship Cargo Used: {ship_cargo_used}\n"
                      f"Ship Cargo Free: {ship_cargo_free}\n"
                        f"---Fuel Info---\n"
                      f"Ship Fuel Capacity: {ship_fuel_capacity}\n"
                      f"Ship Fuel Available: {ship_fuel_available}\n"
                      f"Ship Fuel Burned: {ship_fuel_burned}\n")   
        return ship_symbol, ship_status, ship_flight_mode, ship_system, ship_waypoint, ship_x, ship_y, ship_coord, ship_cargo_capacity, ship_cargo_used, ship_cargo_free, ship_fuel_capacity, ship_fuel_available, ship_fuel_burned
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

get_ship_info("LONESTARTIGER-1")


response = requests.get(url + 'my/ships/LONESTARTIGER-1', headers=headers)
ships_data = response.json()
ship_x = ships_data['data']['nav']['route']['destination']['x']
ship_y = ships_data['data']['nav']['route']['destination']['y']
ship_coord = (ship_x, ship_y)
print(f"Ship Coordinates: {ship_coord}")
print(ship_x)
print(ship_y)
print(json.dumps(ships_data, indent=4))


def euclidean_distance(ship, destination_coord):
    """
    Calculate the Euclidean distance between the ships coordinates and the given destination coordinates.
    :ship: name of the ship of interest, used to pass to get_ship_info to get the ship's coordinates
    :param ship_coord: Tuple of the ship's coordinates (x, y).
    :param destination_coord: Tuple of the destination coordinates (x, y).
    """
    ship_coord = get_ship_info(ship)[7]
    print(f"Ship Coordinates: {ship_coord}")
    print(f"Destination Coordinates: {destination_coord}")
    # Calculate the Euclidean distance
    print(f"Euclidean Distance: {((ship_coord[0] - destination_coord[0]) ** 2 + (ship_coord[1] - destination_coord[1]) ** 2) ** 0.5}")
    # Return the distance
    return ((ship_coord[0] - destination_coord[0]) ** 2 + (ship_coord[1] - destination_coord[1]) ** 2) ** 0.5

#euclidean_distance('LONESTARTIGER-1', (12, -24))



