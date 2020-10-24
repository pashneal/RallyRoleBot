import requests
import json


BASE_URL = "https://api.rally.io/v1"



def get_balances(rally_id):
    return json.loads(requests.get(BASE_URL + "users/rally/" + rally_id + '/balance').json())

def get_balance_of_coin(rally_id, coin_name):
    for coin_balance in get_balances(rally_id):
        if coin_balance["coinKind"] == coin_name:
            return coin_balance["coinBalance"]
    return 0