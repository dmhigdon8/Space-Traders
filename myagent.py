import requests
import json

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yMCIsImlhdCI6MTc0NTM3MTEzOSwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YR2svGz8zTThGdfLvpS6nhX9xgqlzuAxM0SnIRT3-JwlPrw8_z-IcGdxffRXqOVfE4Tf4RKPMLsX0bMzERVJBBkYNLy_cngKAnGTb3xWnPv4GE93jupZSjRmzmt1dXvLnMP6vRaCiO2qP-tHuiBm8gfk3IDyJ9MwRFz-58cJFSYtyFTaDz-FL_fQXRN4kcOPZMTbu-TaSZK-m68TSevr4eIfywyYm31aA7kxYbNxDCXm8EXQJi3g1n8mHfGh9CTPFFBJpdWz7jxqE1p20gqjqVfBSxALCvosjLb4KmsORItv_sCTwVDl2sdYWUbGvxbQNYqphusPTttQ1hfJ_l1fAXnGmlTa0ksQhMx9Eh4rnA8WBU4rL_P6wx05_CkdR7-910CA-l7Kav4wc0R6wM1f50xIYJeN481zkiddoj3T1IhOcDKo3AmkkUlqOjVHlDrBabIkQPvbvRvLrg_bZdIixNEPIa9AliainDoY7dwmu6Q0MAdSaqewIundzfZLDOJGOeSDdw_MPRNGW9ioGxzKgxZaJ4VhjMM5HIfMXDd_z1UY57PugnnUUXEgcPRan_HjCXHSil-xvfy4K2rcrGMu96SFfBCd4U_Jc8mL00yyAJ_bvoenJgpxRFy0V8bQd6lHoyOpj7YrM9yejkYQsMMnT2Fthd8suxj5MdLJw3PuBlE'
header = 'Authorization: Bearer ' + token
headers = {'Authorization': 'Bearer ' + token}
symbol = 'LONESTARTIGER'
faction = 'DOMINION'
url = 'https://api.spacetraders.io/v2/'

#get current location
## Ex: X1-DF55-A1; X1 is the sector, DF55 is the system, A1 is the station
response = requests.get(url + 'my/agent', headers=headers)

if response.status_code == 200:
    json_data = response.json()
    account_id = json_data.get("data").get("accountId")
    headquarters = json_data.get("data").get("headquarters")
    credits = json_data.get("data").get("credits")
    ship_count = json_data.get("data").get("shipCount")

else:
    print(f"Error: {response.status_code}")
    print(response.text)

print(f"Account ID: {account_id}\n"
      f"Headquarters: {headquarters}\n"
      f"Credits: {credits}\n"
      f"Ship Count: {ship_count}\n")

