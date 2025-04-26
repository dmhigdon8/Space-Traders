import requests

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yMCIsImlhdCI6MTc0NTM3MTEzOSwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YR2svGz8zTThGdfLvpS6nhX9xgqlzuAxM0SnIRT3-JwlPrw8_z-IcGdxffRXqOVfE4Tf4RKPMLsX0bMzERVJBBkYNLy_cngKAnGTb3xWnPv4GE93jupZSjRmzmt1dXvLnMP6vRaCiO2qP-tHuiBm8gfk3IDyJ9MwRFz-58cJFSYtyFTaDz-FL_fQXRN4kcOPZMTbu-TaSZK-m68TSevr4eIfywyYm31aA7kxYbNxDCXm8EXQJi3g1n8mHfGh9CTPFFBJpdWz7jxqE1p20gqjqVfBSxALCvosjLb4KmsORItv_sCTwVDl2sdYWUbGvxbQNYqphusPTttQ1hfJ_l1fAXnGmlTa0ksQhMx9Eh4rnA8WBU4rL_P6wx05_CkdR7-910CA-l7Kav4wc0R6wM1f50xIYJeN481zkiddoj3T1IhOcDKo3AmkkUlqOjVHlDrBabIkQPvbvRvLrg_bZdIixNEPIa9AliainDoY7dwmu6Q0MAdSaqewIundzfZLDOJGOeSDdw_MPRNGW9ioGxzKgxZaJ4VhjMM5HIfMXDd_z1UY57PugnnUUXEgcPRan_HjCXHSil-xvfy4K2rcrGMu96SFfBCd4U_Jc8mL00yyAJ_bvoenJgpxRFy0V8bQd6lHoyOpj7YrM9yejkYQsMMnT2Fthd8suxj5MdLJw3PuBlE'
header = 'Authorization: Bearer ' + token
headers = {'Authorization': 'Bearer ' + token}
symbol = 'LONESTARTIGER'
faction = 'DOMINION'
url = 'https://api.spacetraders.io/v2/'
systemSymbol = 'X1-MU86'

#get all waypoints in current system
## Ex: X1-DF55-A1; X1 is the sector, DF55 is the system, A1 is the station
response = requests.get(url + 'systems/' + systemSymbol + '/waypoints', headers=headers)
print(response.text)

if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()

    # Extract the data from the JSON response
    waypoints = json_data.get("data", [])
    waypoint_count = 1

    for waypoint in waypoints:
        waypoint_symbol = waypoint.get("symbol")
        waypoint_type = waypoint.get("type")
        waypoint_x = waypoint.get("x")
        waypoint_y = waypoint.get("y")
        waypoint_coordinates = (waypoint_x, waypoint_y)

        #Begin Orbitals
        orbitals = waypoint.get("orbitals")
        orbital_symbol_list = []
        for item in orbitals:
            orbital_symbol_list.append(item.get("symbol"))
        orbital_amount = len(orbitals)
        print(f"~~~Begin Waypoint {waypoint_count}~~~  \n"
              f"--------About--------\n"
              f"Symbol: {waypoint_symbol} \n"
              f"Type: {waypoint_type} \n"
              f"Coordinates: {waypoint_coordinates}\n"
              f"Orbital Amount: {orbital_amount}")
        if len(orbital_symbol_list) > 0:
              print(f"Orbital List: {orbital_symbol_list}\n")
        
        #Begin Traits
        print("---Traits---\n")
        traits = waypoint.get("traits", [])
        trait_counter = 1
        for trait in traits:
            trait_symbol = trait.get("symbol")
            trait_name = trait.get("name")
            trait_description = trait.get("description")

            print(f"    ---->Begin Trait {trait_counter}\n"
                  f"    Symbol: {trait_symbol} \n"
                  f"    Name: {trait_name}\n"
                  f"    Description: {trait_description}\n"
                  f"    ----<End Trait {trait_counter} \n")
            trait_counter += 1
        print(f"---End Traits---\n")

        print(f"~~~End Waypoint {waypoint_count}~~~\n") 
        waypoint_count += 1
    
else:
    print(f"Error: {response.status_code}")
    print(response.text)