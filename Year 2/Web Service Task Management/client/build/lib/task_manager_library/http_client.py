import requests
from .config import BASE_URL, HEADERS

def get(endpoint:str):
    return requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS)

def post(endpoint:str, json=None):
    return requests.post(f"{BASE_URL}/{endpoint}", json=json, headers=HEADERS)

def put(endpoint:str, json=None):
    return requests.put(f"{BASE_URL}/{endpoint}", json=json, headers=HEADERS)

def delete(endpoint:str):
    return requests.delete(f"{BASE_URL}/{endpoint}", headers=HEADERS)


def terminal_response(response:requests.Response.json):
    if 'message' in response:
        print(response['message'])
    if 'error' in response:
        #print(response['error'])
        raise Exception(response['error'])

    if 'warning' in response:
        print(response['warning'])