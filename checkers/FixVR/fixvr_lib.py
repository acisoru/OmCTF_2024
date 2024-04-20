
import requests

from checklib import *

PORT = 8080

class CheckMachine:
    @property
    def url(self) -> str:
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def register(self, session: requests.Session, email: str, password: str):
        url = f'{self.url}/register'
        response = session.post(url, data={
            "email": email,
            "password": password
        })
        self.c.assert_neq(session.cookies.get("AIOHTTP_SESSION"), None, "Auth cookie(AIOHTTP_SESSION) were not set on registration")
        self.c.assert_eq(200, response.status_code, "invalid response code on registration")	

    def login(self, session: requests.Session, email: str, password: str, status: Status):
        url = f'{self.url}/login'
        response = session.post(url, data={
            "email": email,
            "password": password
        })
        self.c.assert_eq(200, response.status_code, "invalid response code on login", status)

    def create_request(self, session: requests.Session, title: str, description: str, status: Status):
        url = f'{self.url}/api/create-request'
        data = {
            "title": title,
            "description": description
        }
        response = session.post(url, json=data)
        self.c.assert_eq(200, response.status_code, "failed to create request", status)
        return self.c.get_json(response, "Invalid response on creating request", status)

    def get_request(self, session: requests.Session, request_id: int, status: Status) -> dict: 
        url = f'{self.url}/api/requests'
        response = session.get(url)
        data = self.c.get_json(response, "Invalid response on getting request", status)
        self.c.assert_eq(type(data), list, "Invalid response on getting request", status)
        data = next((request for request in data if request['id'] == request_id), None)
        self.c.assert_neq(data, None, "Post was not found on account", status)
        return data
