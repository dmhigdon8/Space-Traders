import json
import requests
import time
import config

# VARIABLES
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNS0xOCIsImlhdCI6MTc0NzcxMzk1OCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.XGItP-gPIvscAw9SwcAFVlFSnLTkWbftYU3b619LjuI8SaX4oyVsA-PyXj35GLYXzZvOWfT96PpSpntw5YTHlnT795vBTXgzBvfh2989AiLXE5dxNpZ32JTgZKm3b2dLim7A2W4n4cn28Dzc7AOUsvr8fNlm1V5GSVvLtotTkyrDc_Q-3xF0HJjVXMg9Nj8f_fV17U6jV-RdeemSMiXPJ7dMlkW9xi3sWOVry2-hzbmkO8FmjNGbxkKMAu-CG1L_FQX7ZeOS2z4vcn475t1Ru7_mB7Z4_pvXfH631CcHuE-gGKLBkY5lI9fU4ccKswpo5P3z25woJGDjtPjxGC1-8-L_iYp4BuWUVi2drOX4Bh3DESO6darTQdi5wuMbLOogYLTAVNEGubXnbuDlJuGFhIL4RyqXTu1zO7TQTi_ox_1rseEhZGczzdZcVw9OA0MP2Gox5vLFzVTeF8u47y0UtHdVbxWW10MnrFlBDlzk4FlA8WnmHhQd0SzUPexsb3XpFLpLi16YjMf79guUX-tJ7VXhtccv3q-mKI_8NwNwotHZac_RJVen65-PnJkQbZAyF6jSqLF_jgShizD84dgylWMS3UeKoRui3XVQLEngbvUiCQXyPAOR0Ix5IuqMe6KpLe9hE0niurzynUx5s3bOqnhGamCLAZu9t67uHvvxXfU'
headers = {'Authorization': 'Bearer ' + token}
url = 'https://api.spacetraders.io/v2/'

class User:
    """defining a class for user"""
    def __init__(self, token, headers, url):
        self.token = token
        self.headers = headers
        self.url = url

class Ship(User):
    """starting a class"""
    def __init__(self, symbol, token, headers, url):#, cargo_capacity, fuel_capacity): 
        super().__init__(token, headers, url) 
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
            self.cargo_capacity = data.get('cargo', {}).get('capacity', 0)
            self.cargo_used = data.get('cargo', {}).get('units', 0)
            self.cargo_free = self.cargo_capacity - self.cargo_used
            self.fuel_capacity = data.get('fuel', {}).get('capacity', 0)
            self.fuel_available = data.get('fuel', {}).get('units', 0)
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
        
    def __str__(self):
        """Return a string representation of the ship."""
        return (f"Ship Name: {self.symbol}, "
                f"Cargo Capacity: {self.cargo_capacity}, "
                f"Fuel Capacity: {self.fuel_capacity}, "
                f"Status: {self.status}")
    




