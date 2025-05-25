import config

ship1 = config.Ship('LONESTARTIGER-1')

print(ship1)

print(ship1.fuel_percentage)

config.find_nearest_fuel_station(ship1.symbol)
dest = config.find_nearest_fuel_station(ship1.symbol)['symbol']
print(f"Nearest fuel station: {dest}")

config.dock_ship(ship1.symbol, dest)
config.refuel_ship(ship1.symbol)
print(f"Fuel after docking: {ship1.fuel_available} units")