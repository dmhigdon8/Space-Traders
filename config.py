# This file contains the configuration for the Space Traders API
import json
import requests
import time

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yNyIsImlhdCI6MTc0NTc4ODU3Miwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YEd-r2hMKjhbDCgTV49HEJ7i_snv5TilYUKpusGLX7uK98cu7k-dW1tlLOvv_cZnIogjE_TpxYZQ9HOTAElhxaLiod4DWpJt5vIaM7SfUW0nrrtSuWbJSAWZi3ne6ySWWa35Ap7wvRuoyUzB4GBzbpCkLUXvJpvg5B9sT5edLYiPsmqU0P_N2UGWw1aqLgy9LGIb8ohMAg6CAs-OjzTNvVEX3XCieBFP8Lc7N9LUMQd5RQLbDEmeu0RP22Uqtv7BBR0Tr8t9e1JC7twRUe7uuu6CK71vqNhTFQzWLaw61k-dQ15mPTTnHhYfT1q8Y_K-Q_r-tF65R35NZvYzD3x2H3XKpJ0baUNE32Gn_zdHiWtMxne4hRspVSvF_VeFROys9DJVBrWYKCujS-yPytuH0YIahwCWFlWd1_UJ9a-bvWEGsXLR2HwrgR3S5UyQTkiz0JjIjpLTJ_me8aNA8oW52ms19rc_-zM989TeMgO01MQh3AngFpgZuAshsV8vf9Oa87Ymz2Fqk3aPBjBW_Akq0QXWpXdaq6sZxkFEXHgo-r-q3gyM112b7Wzxfahh5KVKqpWDEU-bdo6wxCSTXPPBuX2Xi_wKftjP1ko12ptecp8iCDuKQ11y6WNk4mG8VewpBzyRHBrnw8-Etyd_0UPV5x-3nb1I-N3NHclVSdnyXnM'
#header = 'Authorization: Bearer ' + token
headers = {'Authorization': 'Bearer ' + token}
#symbol = 'LONESTARTIGER'
#faction = 'DOMINION'
url = 'https://api.spacetraders.io/v2/'

agent = requests.get(url + 'my/agent', headers=headers)
agent_pretty = json.loads(agent.text)
print(json.dumps(agent_pretty, indent=4))


def get_agent_info():
    """
    Get the agent information.
    """
    response = requests.get(url + 'my/agent', headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        account_id = json_data.get("data").get("accountId")
        symbol = json_data.get("data").get("symbol")
        headquarters = json_data.get("data").get("headquarters")
        credits = json_data.get("data").get("credits")
        faction = json_data.get("data").get("startingFaction")
        ship_count = json_data.get("data").get("shipCount")
        return account_id, symbol, headquarters, credits, faction, ship_count 
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Capture the return values
account_id, symbol, headquarters, credits, faction, ship_count = get_agent_info()

print(get_agent_info())

def get_ship_info():
    """
    Get the ship information.
    """
    response = requests.get(url + 'my/ships', headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        ships = json_data.get("data", [])
        return ships
    else:
        print(f"Error: {response.status_code}")
        print(response.text)



