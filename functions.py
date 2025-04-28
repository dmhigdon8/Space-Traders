import requests
import json
import time
import config

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yNyIsImlhdCI6MTc0NTc4ODU3Miwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YEd-r2hMKjhbDCgTV49HEJ7i_snv5TilYUKpusGLX7uK98cu7k-dW1tlLOvv_cZnIogjE_TpxYZQ9HOTAElhxaLiod4DWpJt5vIaM7SfUW0nrrtSuWbJSAWZi3ne6ySWWa35Ap7wvRuoyUzB4GBzbpCkLUXvJpvg5B9sT5edLYiPsmqU0P_N2UGWw1aqLgy9LGIb8ohMAg6CAs-OjzTNvVEX3XCieBFP8Lc7N9LUMQd5RQLbDEmeu0RP22Uqtv7BBR0Tr8t9e1JC7twRUe7uuu6CK71vqNhTFQzWLaw61k-dQ15mPTTnHhYfT1q8Y_K-Q_r-tF65R35NZvYzD3x2H3XKpJ0baUNE32Gn_zdHiWtMxne4hRspVSvF_VeFROys9DJVBrWYKCujS-yPytuH0YIahwCWFlWd1_UJ9a-bvWEGsXLR2HwrgR3S5UyQTkiz0JjIjpLTJ_me8aNA8oW52ms19rc_-zM989TeMgO01MQh3AngFpgZuAshsV8vf9Oa87Ymz2Fqk3aPBjBW_Akq0QXWpXdaq6sZxkFEXHgo-r-q3gyM112b7Wzxfahh5KVKqpWDEU-bdo6wxCSTXPPBuX2Xi_wKftjP1ko12ptecp8iCDuKQ11y6WNk4mG8VewpBzyRHBrnw8-Etyd_0UPV5x-3nb1I-N3NHclVSdnyXnM'
header = 'Authorization: Bearer ' + token
headers = {'Authorization': 'Bearer ' + token}
ship_symbol = 'LONESTARTIGER-01'
destination = 'X1-MU86-ZZ5F'

#def dock_ship(ship_symbol, destination):
#    """
#    Dock the ship at the specified destination.
#    """
#    dock = requests.post('https://api.spacetraders.io/v2/my/ships/' + ship_symbol + '/dock', headers=headers,
#                         data={'waypointSymbol': destination})
#    dock_pretty = json.loads(dock.text)
#    print(json.dumps(dock_pretty, indent=4))
#    return dock_pretty

#dock_ship(ship_symbol, destination)

print(config.test)