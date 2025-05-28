# This file contains the configuration for the Space Traders, and defines functions for use in other programs

# MODULES
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any, Union

# VARIABLES
token: str = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNS0yNSIsImlhdCI6MTc0ODMxNzc1NCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.ALNy8FaGh6thSV2JiHlJvYl7gf2uIOfu7I4Bh8F076zD-wsYFxPryMEVbtrvYx3C_9XWlHoSZWMoVehm9EePg21WWUS70tUuDigAqcyjtj3mOxt2bFHHPPgdcbDWdSaWMDj5dZHBPRaeugZLy6mNCdQHo33UdeAtgBUdFyEv7poUGLwxIkXG4m-sUaI0i3tp7U96AVXvyXE3pISFESQjF_9vw9GTUueWgFpAAzOTTfTISQsHCB9vf0_izLX15E0ry-80UdP0EJesjlwYwc8vnyKj62WSvLzYHbZWl-OqbAtK-k668SYcCR9fJ3G-oSfhyd_PwlfXNPYldFcc7nFxEnQL7S1LnQEIxefTZ8l6M_HrNQWggmmHbxk0pf7dVqVybtNUCRD0-DrFN3x3ewp0tubkCmbmNZd1w3NloGj-56ogIpNSBuABc7nm6XKzQdSdMYltnEbL12hZvyFf1iHaB9A89owXIaFRLU0YqRqPyEbJhnQ_wj6becpyOWpzg4EkMZi4LnsytA61ZSCEjAiDNoxBJaKCv5La8NUbnABeFUyzSlRWA3KdOkL57uPFtf8_eLlEC2nBxOSxxbP5NH7SJgmBR2hjIpSxhr6jDvHW9ViCt_xpwBN7wHvnFk9ZsiH0YyMbNoeX0zzXLqnAXb-B_i_40mv36G-PFsEqsxId26o'
headers: Dict[str, str] = {'Authorization': 'Bearer ' + token}
url: str = 'https://api.spacetraders.io/v2/'
response: requests.Response = requests.get(url + 'my/ships', headers=headers)
player_name: str = 'LONESTARTIGER'
start_of_current_week = datetime.now() - timedelta(days=datetime.now().weekday())  # Monday of the current week
str_start_of_current_week: str = start_of_current_week.strftime('%Y-%m-%d')
print(f"Start of current week: {start_of_current_week.strftime('%Y-%m-%d')}")




# SETUP
def get_api_credentials() -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Creates a dictionary to store the API credentials.
    """
    return {
        "token": token,
        "headers": headers,
        "url": url
    }

# BASE CLASSES
class User:
    """defining a class for user"""
    def __init__(self) -> None:
        creds: Dict[str, Union[str, Dict[str, str]]] = get_api_credentials()
        self.token: str = creds['token']
        self.headers: Dict[str, str] = creds['headers']
        self.url: str = creds['url']

    def see_contracts(self) -> Optional[Dict[str, Any]]:
        """
        Fetches the user's contracts from the API.
        """
        try:
            response = requests.get(f"{self.url}my/contracts", headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json().get('data', {})
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        
    def accept_first_contract(self) -> Optional[Dict[str, Any]]:
        """
        Accepts the first contract by its ID.
        :param contract_id: The ID of the contract to accept.
        """
        data = self.see_contracts()
        contract_id = data[0].get('id')
        try:
            response = requests.post(f"{self.url}my/contracts/{contract_id}/accept", headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json().get('data', {})
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

class Ship(User):
    """starting a class"""
    def __init__(self, symbol): 
        super().__init__() 
        self.symbol = symbol
        self.cargo_capacity = None
        self.cargo_used = None
        self.cargo_free = None
        self.fuel_capacity = None 
        self.fuel_available = None
        self.fuel_user = None
        self.fuel_percentage = None
        self.status = None
        self.flight_mode = None
        self.system = None
        self.ship_role = None
        self.ship_x = None
        self.ship_y = None
        self.ship_coordinates = None
        self.fetch_ship_data()  

    def fetch_ship_data(self):
        """Fetch ship data from the API and update the instance variables."""
        try:
            response = requests.get(f"{self.url}my/ships/{self.symbol}", headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json().get('data', {})  
            print(json.dumps(data, indent=4))  # Debugging line to see the raw data
            self.cargo_capacity = data.get('cargo', {}).get('capacity', 0)
            self.cargo_used = data.get('cargo', {}).get('units', 0)
            self.cargo_free = self.cargo_capacity - self.cargo_used
            self.fuel_capacity = data.get('fuel', {}).get('capacity', 0)
            self.fuel_available = data.get('fuel', {}).get('current', 0)
            self.fuel_used = self.fuel_capacity - self.fuel_available
            self.fuel_percentage = round(self.fuel_available / self.fuel_capacity, 2) * 100 if self.fuel_capacity > 0 else 0
            self.status = data.get('nav', {}).get('status', 'UNKNOWN')
            self.flight_mode = data.get('nav', {}).get('flightMode', 'UNKNOWN')
            self.system = data.get('nav', {}).get('systemSymbol', 'UNKNOWN')
            self.ship_role = data.get('role', 'UNKNOWN')
            self.ship_x = data.get('nav', {}).get('route', {}).get('destination', {}).get('x', 'UNKNOWN')
            self.ship_y = data.get('nav', {}).get('route', {}).get('destination', {}).get('y', 'UNKNOWN')
            self.ship_coordinates = (data.get('nav', {}).get('route', {}).get('destination', {}).get('x', 'UNKNOWN'), data.get('nav', {}).get('route', {}).get('destination', {}).get('y', 'UNKNOWN'))
            return data
        except requests.exceptions.RequestException as e:
            print(f"API request failed with status code {response.status_code}: {e}") 
            return None
        
    def get_ship_status(self) -> Dict[str, Any]:
        """
        Get the current status of the ship.
        :return: A dictionary containing the ship's status and other details.
        """
        try:
            response = requests.get(f"{self.url}my/ships/{self.symbol}", headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json().get('data', {})
            return f"Ship Status: {data.get('nav', {}).get('status', 'UNKNOWN')}, " \
                   f"Flight Mode: {data.get('nav', {}).get('flightMode', 'UNKNOWN')}, " 
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}
        
    def navigate_to_waypoint(self, waypoint_symbol: str) -> Optional[Dict[str, Any]]:
        """
        Navigate the ship to a specified waypoint.
        :param waypoint_symbol: The symbol of the waypoint to navigate to.
        """
        try:
            response = requests.post(f"{self.url}my/ships/{self.symbol}/navigate", headers=self.headers, json={"waypointSymbol": waypoint_symbol})
            response.raise_for_status()  # Raise an error for bad responses
            return response.json().get('data', {})
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        
    def __str__(self):
        """Return a string representation of the ship."""
        return (f"Ship Name: {self.symbol}, "
                f"Cargo Capacity: {self.cargo_capacity}, "
                f"Cargo Used: {self.cargo_used}, "
                f"Cargo Free: {self.cargo_free}, "
                f"Fuel Capacity: {self.fuel_capacity}, "
                f"Fuel Available: {self.fuel_available}, "
                f"Status: {self.status}")

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
        ship_info = {
        'ship_symbol' : ships_data['data']['symbol'],
        'ship_status' : ships_data['data']['nav']['status'],
        'ship_flight_mode' : ships_data['data']['nav']['flightMode'],
        'ship_system' : ships_data['data']['nav']['systemSymbol'],
        'ship_waypoint' : ships_data['data']['nav']['waypointSymbol'],
        'ship_x' : ships_data['data']['nav']['route']['destination']['x'],
        'ship_y' : ships_data['data']['nav']['route']['destination']['y'],
        'ship_coord' : (ships_data['data']['nav']['route']['destination']['x'], ships_data['data']['nav']['route']['destination']['y']),
        'ship_cargo_capacity' : ships_data['data']['cargo']['capacity'],
        'ship_cargo_used' : ships_data['data']['cargo']['units'],
        'ship_cargo_free' : ships_data['data']['cargo']['capacity'] - ships_data['data']['cargo']['units'],
        'ship_fuel_capacity' : ships_data['data']['fuel']['capacity'],
        'ship_fuel_available' : ships_data['data']['fuel']['current'],
        'ship_fuel_burned' : ships_data['data']['fuel']['capacity'] - ships_data['data']['fuel']['current']
        }
        return ship_info
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

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


def print_ship_info(ship):
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
        return print(f"Ship Symbol: {ship_symbol}\n"
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
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def dock_ship(ship, destination=None):
    """
    Dock the ship at the specified destination. If a destination is not provided, the ship will dock at the current waypoint.
    :param ship: The symbol of the ship to dock.
    :param destination: The symbol of the destination waypoint. If not provided, the ship will dock at the current waypoint.
    """
    if destination is None:
        destination = get_ship_info(ship)['ship_waypoint']
    if not isinstance(ship, str):
        try:
            ship = str(ship)
        except (ValueError, TypeError):
            print("Invalid ship symbol. Please provide a valid string.")
            return None
    #force the parameter to be uppercase
    ship = ship.upper()   
    dock = requests.post(url + 'my/ships/' + ship + '/dock', headers=headers,
                         data={'waypointSymbol': destination})
    return f"Ship status: {get_ship_info(ship)['ship_status']}."



def refuel_ship(ship):    # refueling ship
    print(f"Beginning refueling at {get_ship_info(ship)['ship_waypoint']}.\n")
    fuel = requests.post('https://api.spacetraders.io/v2/my/ships/' + get_ship_info(ship)['ship_symbol'] + '/refuel', headers=headers)
    fuel_pretty = json.loads(fuel.text)
    if fuel.status_code != 200:
        error = fuel.json()
        if error['error']['code'] == 'INSUFFICIENT_FUNDS':
            result = "Error: Insufficient funds to refuel."
        elif error['error']['code'] == 'NOT_ENOUGH_FUEL':
            result = "Error: Not enough fuel to refuel."
        elif error['error']['code'] == 'NOT_IN_ORBIT':
            result = "Error: Ship is not in orbit."
        else:
            result = error['error']['message']
    else:
        result = f"""Refueling successful at {get_ship_info(ship)['ship_waypoint']}.
                        Units of fuel purchased: {fuel_pretty['data']['transaction']['units']}
                        Price per unit: {fuel_pretty['data']['transaction']['pricePerUnit']}
                        Total cost: {fuel_pretty['data']['transaction']['totalPrice']}
                      Refuel complete."""
    return result


def launch_to_orbit(ship):  # back to orbit for travel
    print(f"Undocking ship from {get_ship_info(ship)['ship_waypoint']}.\n")
    orbit = requests.post('https://api.spacetraders.io/v2/my/ships/' + get_ship_info(ship)['ship_symbol'] + '/orbit', headers=headers)
    if orbit.status_code != 200:
        error = orbit.json()
        result = error['error']['message']
    else:
        result = (f"    Ship status: {get_ship_info(ship)['ship_status']}\n"
                  f"    Ship waypoint: {get_ship_info(ship)['ship_waypoint']}\n"
                  f"    Ship coordinates: {get_ship_info(ship)['ship_coord']}\n\n"
                  f"Successfully launched to orbit.\n")
    return result


def euclidean_distance(ship, destination_coord):
    """
    Calculate the Euclidean distance between the ships coordinates and the given destination coordinates.
    :ship: name of the ship of interest, used to pass to get_ship_info to get the ship's coordinates
    :param ship_coord: Tuple of the ship's coordinates (x, y).
    :param destination_coord: Tuple of the destination coordinates (x, y).
    """
    ship_coord = get_ship_info(ship)['ship_coord']
    #print(f"Ship Coordinates: {ship_coord}")
    #print(f"Destination Coordinates: {destination_coord}")
    # Calculate the Euclidean distance
    #print(f"Euclidean Distance: {((ship_coord[0] - destination_coord[0]) ** 2 + (ship_coord[1] - destination_coord[1]) ** 2) ** 0.5}")
    # Return the distance
    return ((ship_coord[0] - destination_coord[0]) ** 2 + (ship_coord[1] - destination_coord[1]) ** 2) ** 0.5

def get_fuel_stations(systemSymbol):
    """
    Gets all of the available places to refuel in the system.
    To do this, it first goes though all of the market places and checks if they have fuel as a trade good.
    Then it goes through all of the fuel stations and adds them to the list.
    Finally, it combines the two lists and returns them.
    """
    #begin by getting marketplaces with fuel as a trade good
    response = requests.get(url + 'systems/' + systemSymbol + '/waypoints', headers=headers)
    #print(response.text)
    json_data = response.json()
    waypoints = json_data.get("data", [])
    #print(json.dumps(waypoints, indent=4))

    fuel_marketplaces = []
    for waypoint in waypoints:
        for trait in waypoint.get("traits", []):       
            if trait.get("symbol") == "MARKETPLACE":
                trade_goods_response = requests.get(f'https://api.spacetraders.io/v2/systems/{systemSymbol}/waypoints/{waypoint.get("symbol")}/market', headers=headers)
                trade_goods_json = trade_goods_response.json()
                trade_goods = trade_goods_json.get("data", {}).get("exchange", [])
                for trade_good in trade_goods:
                    if trade_good['symbol'] == "FUEL":
                        fuel_waypoint_data = {
                            "symbol": waypoint.get("symbol"),
                            "x": waypoint.get("x"),
                            "y": waypoint.get("y"),
                            "coordinates": (waypoint.get("x"), waypoint.get("y")),
                            "type": "MARKETPLACE"
                        }
                        fuel_marketplaces.append(fuel_waypoint_data)

    #then get all fuel stations
    response = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + 'FUEL_STATION', headers=headers)
    json_data = response.json()
    fuel_stations = json_data.get("data", [])

    fuel_station_list = []
    for fuel_station in fuel_stations:
        fuel_station_data = {
            "symbol": fuel_station.get("symbol"),
            "x": fuel_station.get("x"),
            "y": fuel_station.get("y"),
            "coordinates": (fuel_station.get("x"), fuel_station.get("y")),
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


def find_nearest_fuel_station(ship): #, systemsymbol):
    """
    Takes a ship and a system symbol and returns the nearest fuel station.
    """
    all_system_fuel_stations = get_fuel_stations(get_ship_info(ship)['ship_system'])
    ship_coord = get_ship_info(ship)['ship_coord']
    fuel_stations = []
    for fuel_station in all_system_fuel_stations:
        fuel_station_coord = fuel_station['coordinates']
        distance = (euclidean_distance(ship, fuel_station['coordinates'])) 
        fuel_station_data = {
            "symbol": fuel_station['symbol'],
            "coordinates": (fuel_station['x'], fuel_station['y']),
            "distance": distance
        }
        fuel_stations.append(fuel_station_data)
        #print(f"Fuel Station: {fuel_station['symbol']}; {fuel_station['coordinates']}; Distance: {distance}")   
    closest_station = min(fuel_stations, key=lambda x: x['distance'])
    #print(f"Closest Station: {closest_station['symbol']}; {closest_station['coordinates']}; Distance: {closest_station['distance']}")   
    return closest_station


import json
import requests
response = requests.get(f"{url}my/ships/LONESTARTIGER-1", headers=headers)
response.raise_for_status()  # Raise an error for bad responses
data = response.json().get('data', {})  
print(json.dumps(data, indent=4))  # Debugging line to see the raw data



