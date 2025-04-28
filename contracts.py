import config
import requests
import json

#token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9ORVNUQVJUSUdFUiIsInZlcnNpb24iOiJ2Mi4zLjAiLCJyZXNldF9kYXRlIjoiMjAyNS0wNC0yMCIsImlhdCI6MTc0NTM3MTEzOSwic3ViIjoiYWdlbnQtdG9rZW4ifQ.YR2svGz8zTThGdfLvpS6nhX9xgqlzuAxM0SnIRT3-JwlPrw8_z-IcGdxffRXqOVfE4Tf4RKPMLsX0bMzERVJBBkYNLy_cngKAnGTb3xWnPv4GE93jupZSjRmzmt1dXvLnMP6vRaCiO2qP-tHuiBm8gfk3IDyJ9MwRFz-58cJFSYtyFTaDz-FL_fQXRN4kcOPZMTbu-TaSZK-m68TSevr4eIfywyYm31aA7kxYbNxDCXm8EXQJi3g1n8mHfGh9CTPFFBJpdWz7jxqE1p20gqjqVfBSxALCvosjLb4KmsORItv_sCTwVDl2sdYWUbGvxbQNYqphusPTttQ1hfJ_l1fAXnGmlTa0ksQhMx9Eh4rnA8WBU4rL_P6wx05_CkdR7-910CA-l7Kav4wc0R6wM1f50xIYJeN481zkiddoj3T1IhOcDKo3AmkkUlqOjVHlDrBabIkQPvbvRvLrg_bZdIixNEPIa9AliainDoY7dwmu6Q0MAdSaqewIundzfZLDOJGOeSDdw_MPRNGW9ioGxzKgxZaJ4VhjMM5HIfMXDd_z1UY57PugnnUUXEgcPRan_HjCXHSil-xvfy4K2rcrGMu96SFfBCd4U_Jc8mL00yyAJ_bvoenJgpxRFy0V8bQd6lHoyOpj7YrM9yejkYQsMMnT2Fthd8suxj5MdLJw3PuBlE'
#header = 'Authorization: Bearer ' + token
#headers = {'Authorization': 'Bearer ' + token}
#symbol = 'LONESTARTIGER'
#faction = 'DOMINION'
#url = 'https://api.spacetraders.io/v2/'

response = requests.get(config.url + 'my/contracts', headers=config.headers)
json_data = response.json()
print(json_data)

if response.status_code == 200:
    contract_count = 1
    json_data = response.json()
    contracts = json_data.get("data", [])
    print(type(contracts))

    for contract in contracts:
        contract_id = contract.get("id")
        contract_type = contract.get("type")
        contract_status = contract.get("status")
        contract_faction = contract.get("faction")
        contract_terms_payment_onaccepted = contract.get("terms").get("payment").get("onAccepted")
        contract_terms_payment_onfulfilled = contract.get("terms").get("payment").get("onFulfilled")
        contract_terms_deadline = contract.get("terms").get("deadline")
        payment_total = int(contract_terms_payment_onaccepted) + int(contract_terms_payment_onfulfilled)
        ##iterate through this list?
        for deliverable in contract.get("terms").get("deliver"):
            deliverable_tradesymbol = deliverable.get("tradeSymbol")
            deliverable_quantity = deliverable.get("unitsRequired")
            deliverable_unitsfulfilled = deliverable.get("unitsFulfilled")
            deliverable_destination = deliverable.get("destinationSymbol")


        print(f"~~~Begin Contract {contract_count}~~~\n\n"
              f"--------About--------\nContract ID: {contract_id} \nType: {contract_type} \nStatus: {contract_status}\nFaction: {contract_faction}\n"
              f"--------Terms--------\nPayment on Accepted: {contract_terms_payment_onaccepted} \nPayment on Fulfilled: {contract_terms_payment_onfulfilled} \nPayment Total: {payment_total}\nDeadline: {contract_terms_deadline}\n"
              f"----Deliverables-----\n"
              f"Trade Symbol: {deliverable_tradesymbol} \nQuantity Required: {deliverable_quantity} \nUnits Fulfilled: {deliverable_unitsfulfilled} \nDestination: {deliverable_destination}\n"
              f"\n~~~End Contract {contract_count}~~~\n")
        
        contract_count += 1
else:
    print(f"Error: {response.status_code}")
    print(response.text)


## accept contract
accept_contract = requests.post(config.url + 'my/contracts/' + contract_id + '/accept', headers=config.headers)  
print(accept_contract.text)

