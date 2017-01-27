import requests
import json

def login(email, password):
    "logins and gets the id token"

    response = requests.post('https://locs-stag.swiq3.com/api/users/login',
                             json={'email': email, 'password': password})
    return response.json()

def push(authentication_id, request_data):
    "sends the data to the server"
    return requests.post('https://locs-stag.swiq3.com/api/pois/push',
                         json=request_data,
                         headers={'Authorization': authentication_id})
