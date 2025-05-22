import json
import requests
import time

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

User = User(token, headers, url)
# Print the attributes of the User class
# This will print the token, headers, and url
print("User class attributes:")
print("Token:", User.token)
print("Headers:", User.headers)
print("URL:", User.url)    

#print(User.token)
#print(User.headers)
#print(User.url)     


class ship:
    """starting a class"""
    def __init__(self, name):#, cargo_capacity, fuel_capacity):
        self.name = name.upper()
        #self.cargo_capacity = cargo_capacity
        #self.fuel_capacity = fuel_capacity

    def get_cargo_capacity(self):
        if not isinstance(self.name, str):
            print("Invalid ship symbol. Please provide a valid string.")
            return None
        
        response = requests.get(f"{url}my/ships/{self.name}", headers=headers)
        if response.status_code == 200:
            try:
                ships_data = response.json()
                return ships_data['data']['cargo']['capacity']
            except (KeyError, ValueError) as e:
                print(f"Error parsing ship data: {e}")
                return None
   
        else:
            print(f"API request failed with status code: {response.status_code}: {response.text}")
            return None
        
    def get_fuel_capacity(self):
        if not isinstance(self.name, str):
            print("Invalid ship symbol. Please provide a valid string.")
            return None
        
        response = requests.get(f"{url}my/ships/{self.name}", headers=headers)
        if response.status_code == 200:
            try:
                ships_data = response.json()
                return ships_data['data']['fuel']['capacity']
            except (KeyError, ValueError) as e:
                print(f"Error parsing ship data: {e}")
                return None
        else:
            print(f"API request failed with status code: {response.status_code}: {response.text}")
            return None

    def get_current_fuel(self):
        if not isinstance(self.name, str):
            print("Invalid ship symbol. Please provide a valid string.")
            return None
            
        response = requests.get(f"{url}my/ships/{self.name}", headers=headers)
        if response.status_code == 200:
            try:
                ships_data = response.json()
                return ships_data['data']['fuel']['current']
            except (KeyError, ValueError) as e:
                print(f"Error parsing ship data: {e}")
                return None
        else:
            print(f"API request failed with status code: {response.status_code}: {response.text}")
            return None
            
        
    
ship1 = ship('LONESTARTIGER-1')

print(ship1.get_cargo_capacity())
print(ship1.get_fuel_capacity())
print(ship1.get_current_fuel())
  
