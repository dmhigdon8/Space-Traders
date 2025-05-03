# This file contains the configuration for the Space Traders API

# MODULES
import json
import requests
import time

# VARIABLES
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yNyIsImlhdCI6MTc0NTc4ODU3Miwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YEd-r2hMKjhbDCgTV49HEJ7i_snv5TilYUKpusGLX7uK98cu7k-dW1tlLOvv_cZnIogjE_TpxYZQ9HOTAElhxaLiod4DWpJt5vIaM7SfUW0nrrtSuWbJSAWZi3ne6ySWWa35Ap7wvRuoyUzB4GBzbpCkLUXvJpvg5B9sT5edLYiPsmqU0P_N2UGWw1aqLgy9LGIb8ohMAg6CAs-OjzTNvVEX3XCieBFP8Lc7N9LUMQd5RQLbDEmeu0RP22Uqtv7BBR0Tr8t9e1JC7twRUe7uuu6CK71vqNhTFQzWLaw61k-dQ15mPTTnHhYfT1q8Y_K-Q_r-tF65R35NZvYzD3x2H3XKpJ0baUNE32Gn_zdHiWtMxne4hRspVSvF_VeFROys9DJVBrWYKCujS-yPytuH0YIahwCWFlWd1_UJ9a-bvWEGsXLR2HwrgR3S5UyQTkiz0JjIjpLTJ_me8aNA8oW52ms19rc_-zM989TeMgO01MQh3AngFpgZuAshsV8vf9Oa87Ymz2Fqk3aPBjBW_Akq0QXWpXdaq6sZxkFEXHgo-r-q3gyM112b7Wzxfahh5KVKqpWDEU-bdo6wxCSTXPPBuX2Xi_wKftjP1ko12ptecp8iCDuKQ11y6WNk4mG8VewpBzyRHBrnw8-Etyd_0UPV5x-3nb1I-N3NHclVSdnyXnM'
headers = {'Authorization': 'Bearer ' + token}
url = 'https://api.spacetraders.io/v2/'

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
                        f"---Cargo Info---\n"
                      f"Ship Cargo Capacity: {ship_cargo_capacity}\n"
                      f"Ship Cargo Used: {ship_cargo_used}\n"
                      f"Ship Cargo Free: {ship_cargo_free}\n"
                        f"---Fuel Info---\n"
                      f"Ship Fuel Capacity: {ship_fuel_capacity}\n"
                      f"Ship Fuel Available: {ship_fuel_available}\n"
                      f"Ship Fuel Burned: {ship_fuel_burned}\n")   
        return ship_symbol, ship_status, ship_flight_mode, ship_system, ship_waypoint, ship_cargo_capacity, ship_cargo_used, ship_cargo_free, ship_fuel_capacity, ship_fuel_available, ship_fuel_burned
    else:
        print(f"Error: {response.status_code}")
        print(response.text)




