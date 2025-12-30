
# MODULES
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Any, Union
import time

# VARIABLES
test = 'test'
test2 = 'test2'
test3 = 'test3'
print(test3)
print(test2)
token: str = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNi0wMSIsImlhdCI6MTc0ODgzOTc1MCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.ga1o-XcqagQEj1DQ0WpH_s_4e8eQm5HdNlKWZrLwg7D8zP5-aYGHdr4jXqcQF5kRW4DW3TMjC_h7yj5JzMieBTJbG_a549jQ7HlaUbMbMjrQvyku-UlupmrCAIi7WfpVaBgB9zJiRXqPSxHEISsVH2GEXDpv7VCY_eoBmKpmjURhNadNygWIVmqhHV1xzX-8JRNtNaAQzv35wS5yBQ2pMroYm8b64kJROmM1YzRUr5tVxcvD0EezNJV9ew8E67W_GSbq0YgGtTT6oBJHmEL0ISCOnOuOE2aWTRnAi9jq76Z5Ooko8yH45dnxAyjtE8JR8US7e3yGE5iP3Ts02v0ne3JcX9yw_gkq3IHZCa7Xy8uHWSoZGkF7yIcqFIcbxTJxnDk4wEn6v2uOt8JB6M6qwxqJYlqDSl2mImC9z5jfgK2zJ-oM_pkPKfqdtR9ldud2oCcflXRPM4xmZ5k_vW4SYbrANCwVZZ5ceUwAi6ZSyMZJhkHED0FRN5CL0khriX-TgwLaUyJP5IWdTBmJYwIGY_jZr-4iG-KHC9vLOaHQ61C1njdRt7UHSM1QvkY4vC7IAAtK0dn7gXVkgvDckXSkf5SQZmaOPf4o9id8lAhOGC156rfJagE_rgTj0ShmWFJliwrqUQeLG6M0aHLCCrqDRFrRT6VCDP32kTrQ5czMR3Y'
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
            self.ship_waypoint = data.get('nav', {}).get('waypointSymbol', 'UNKNOWN')
            self.ship_x = data.get('nav', {}).get('route', {}).get('destination', {}).get('x', 'UNKNOWN')
            self.ship_y = data.get('nav', {}).get('route', {}).get('destination', {}).get('y', 'UNKNOWN')
            self.ship_coordinates = (data.get('nav', {}).get('route', {}).get('destination', {}).get('x', 'UNKNOWN'), data.get('nav', {}).get('route', {}).get('destination', {}).get('y', 'UNKNOWN'))
            return data
        except requests.exceptions.RequestException as e:
            print(f"API request failed with status code {response.status_code}: {e}") 
            return None

ship_test = Ship('LONESTARTIGER-1')
        
    def mine(self, item_symbol: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Perform mining and optionally jettison items not matching the specified item_symbol.
        :param item_symbol: If provided, only keep items with this symbol, jettison others.
        :param max_attempts: Maximum number of mining attempts to prevent infinite loops.
        :return: Dictionary with mining results or None if failed.
        """
        #check cargo hold post mining
        #cargo = requests.get('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/cargo', headers=config.headers)
        #cargo_pretty = json.loads(cargo.text)
        #print(json.dumps(cargo_pretty, indent=4))

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
            #replace with variable as last step
            time.sleep(80)
        


