import requests

from checklib import *

PORT = 5000

class CheckMachine:
    @property
    def url(self) -> str:
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def signup(self, session: requests.Session, email: str, password: str, status: Status):
        url = f'{self.url}/signup'
        response = session.post(url, json={
            "username": email,
            "password": password
        })
        self.c.assert_eq(response.json()["server_resp"], "User registered successfully", "fail to register", status)
        self.c.assert_eq(200, response.status_code, "invalid response code on signup", status)	

    def signin(self, session: requests.Session, email: str, password: str, status: Status):
        url = f'{self.url}/signin'
        response = session.post(url, json={
            "username": email,
            "password": password
        })

        session.cookies.set("id", str(response.json()["id"]))
        session.cookies.set("token", response.json()["token"])

        self.c.assert_eq(200, response.status_code, "invalid response code on signin", status)

    def signout(self, session: requests.Session, status: Status):
        url = f'{self.url}/signout'
        response = session.post(url, json={
            "id": int(session.cookies.get_dict()["id"]),
            "token": session.cookies.get_dict()["token"]
        })

        session.cookies.clear()

        self.c.assert_eq(200, response.status_code, "invalid response code on signout", status)
        self.c.assert_eq(response.json()["success"], True, "invalid signout", status)

    def createclone(self, session: requests.Session, cloneUUID: str, description: str, status: Status):
        url = f'{self.url}/createclone'
        data = {
            "id": int(session.cookies.get_dict()["id"]),
            "token": session.cookies.get_dict()["token"],
            "cloneUUID": cloneUUID,
            "description": description
        }
        response = session.post(url, json=data)
        self.c.assert_eq(200, response.status_code, "failed to create clone", status)
        self.c.assert_eq(True, response.json()["success"], "Error while creating clone", status)

    def getclones(self, session: requests.Session, user_id: int, status: Status) -> list: 
        url = f'{self.url}/getclones'
        response = session.post(url, json={
            "my_id": int(session.cookies.get_dict()["id"]),
            "token": session.cookies.get_dict()["token"],
            "user_id": int(user_id)
        })
        data = self.c.get_json(response, "Invalid response on getting clones", status)
        self.c.assert_eq(type(data), dict, "Invalid response on getting request", status)
        self.c.assert_neq(data, None, "Clones not found", status)
        return data
    

    def createclonefromurl(self, session: requests.Session, url_r: str, status: Status):
        url = f'{self.url}/createclonefromurl'
        data = {
            "id": int(session.cookies.get_dict()["id"]),
            "token": session.cookies.get_dict()["token"],
            "url": url_r
        }
        response = session.post(url, json=data)
        self.c.assert_eq(200, response.status_code, "failed to create request", status)
        self.c.assert_eq(True, response.json()["success"], "Error while creating clone", status)