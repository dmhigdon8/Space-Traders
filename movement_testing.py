import config
import requests
import json
import time


#STEPS# 1. Create a ship instance with the symbol 'LONESTARTIGER-1'.
gt = config.User()

# 2. Print the ship's details.
ship1 = config.Ship('LONESTARTIGER-1')
print(ship1.fuel_percentage)

# 3. Check contracts and accept
gt.see_contracts()
gt.accept_first_contract()

# 4. Store item the contract is for
contract_item = gt.see_contracts()[0]['terms']['deliver'][0]['tradeSymbol']
contract_quantity = gt.see_contracts()[0]['terms']['deliver'][0]['unitsRequired']
contract_delivery_location = gt.see_contracts()[0]['terms']['deliver'][0]['destinationSymbol'] 
print(f"Contract item: {contract_item}, Quantity: {contract_quantity}, Delivery Location: {contract_delivery_location}")


# 5. Find item/asteroid to mine for the item
location_type = 'ENGINEERED_ASTEROID'
systemSymbol = ship1.system
engineered_asteroid = requests.get('https://api.spacetraders.io/v2/systems/' + systemSymbol + '/waypoints?type=' + location_type, headers=config.headers).json()['data'][0]['symbol']

# 6. Undock and travel to the asteroid
config.launch_to_orbit(ship1.symbol)

# 7. Travel to the asteroid
ship1.navigate_to_waypoint(engineered_asteroid)
print(ship1.get_ship_status())
print(ship1.get_ship_location())

# 8. Mine the asteroid for the item
# need to fix this, it's not working, also should add in logic to navigate to sell/deliver items once cargo is full
#test
ship1.mine(contract_item)

import requests
token: str = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNS0yNSIsImlhdCI6MTc0ODMxNzc1NCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.ALNy8FaGh6thSV2JiHlJvYl7gf2uIOfu7I4Bh8F076zD-wsYFxPryMEVbtrvYx3C_9XWlHoSZWMoVehm9EePg21WWUS70tUuDigAqcyjtj3mOxt2bFHHPPgdcbDWdSaWMDj5dZHBPRaeugZLy6mNCdQHo33UdeAtgBUdFyEv7poUGLwxIkXG4m-sUaI0i3tp7U96AVXvyXE3pISFESQjF_9vw9GTUueWgFpAAzOTTfTISQsHCB9vf0_izLX15E0ry-80UdP0EJesjlwYwc8vnyKj62WSvLzYHbZWl-OqbAtK-k668SYcCR9fJ3G-oSfhyd_PwlfXNPYldFcc7nFxEnQL7S1LnQEIxefTZ8l6M_HrNQWggmmHbxk0pf7dVqVybtNUCRD0-DrFN3x3ewp0tubkCmbmNZd1w3NloGj-56ogIpNSBuABc7nm6XKzQdSdMYltnEbL12hZvyFf1iHaB9A89owXIaFRLU0YqRqPyEbJhnQ_wj6becpyOWpzg4EkMZi4LnsytA61ZSCEjAiDNoxBJaKCv5La8NUbnABeFUyzSlRWA3KdOkL57uPFtf8_eLlEC2nBxOSxxbP5NH7SJgmBR2hjIpSxhr6jDvHW9ViCt_xpwBN7wHvnFk9ZsiH0YyMbNoeX0zzXLqnAXb-B_i_40mv36G-PFsEqsxId26o'
headers = {'Authorization': 'Bearer ' + token}
response = requests.get(f"https://api.spacetraders.io/v2/my/contracts", headers=headers)
response.raise_for_status()  # Raise an error for bad response
data = response.json().get('data')
first_contract = data[0].get('id')
print(first_contract)  # Adjusted to get 'id' directly
print(type(first_contract))
print(type(data))
print(type(response))
print(data)
print(data.get('id', 'No ID found'))


mining_attempts = 1
    while True:
        #perform mining
        #mine = requests.post(f"{self.url}my/ships/{self.symbol}/extract", headers=headers)
        mine = requests.post(f"https://api.spacetraders.io/v2/my/ships/LONESTARTIGER-1/extract", headers=headers)
        mine_pretty = json.loads(mine.text)
        cooldown_data = response.json().get('data', {})
        ship_cooldown = cooldown_data.get('cooldown', {}).get('totalSeconds', 0)
        print(json.dumps(mine_pretty, indent=4))

        #check cargo hold post mining
        cargo = requests.get(f"https://api.spacetraders.io/v2/my/ships/LONESTARTIGER-1/cargo", headers=headers)
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
                jettison = requests.post('https://api.spacetraders.io/v2/my/ships/' + 'LONESTARTIGER-1' + '/jettison', headers=config.headers, json={'symbol': jettison_symbol, 'units': jettison_units})
        
        if cargo_units_used >= cargo_units:
            print("Cargo hold is full, stopping mining.")
            break
        print(f"Mining attempt {mining_attempts}\n")
        mining_attempts += 1
        time.sleep(ship_cooldown)



