#!/usr/bin/env python3
import sys
import os
import requests
import random

from checklib import *
from fixvr_lib import *
from pathlib import Path

BASE_DIR = Path(__file__).absolute().resolve().parent

class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 5
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests.exceptions.ConnectionError')

    def check(self):
        session = self.get_initialized_session()
        email, password = f"{rnd_username()}@mail.ru", rnd_password() 

        title = rnd_string(15)
        description = rnd_string(20)

        self.mch.register(session, email, password)
        self.mch.login(session, email, password, Status.MUMBLE)

        created_request = self.mch.create_request(session, title=title, description=description, status=Status.MUMBLE)

        data = self.mch.get_request(session, request_id=created_request["request"]["id"], status=Status.MUMBLE)
        self.assert_eq(data["title"], title, "Title value is invalid", Status.CORRUPT)
        self.assert_eq(data["description"], description, "Description value is invalid", Status.CORRUPT)
        self.cquit(Status.OK)

        #check if registered+logined, request is created and title/description are not changed


    def put(self, flag_id: str, flag: str, vuln: str):
        session = self.get_initialized_session()
        email, password = f"{rnd_username()}@mail.ru", rnd_password() 
        self.mch.register(session, email, password)
        self.mch.login(session, email, password, Status.MUMBLE)

        if vuln == "1":
            for i in range(random.randint(1, 4)):
                title = rnd_string(15)
                description = rnd_string(20)
                self.mch.create_request(session, title=title, description=description, status=Status.MUMBLE)
            created_request = self.mch.create_request(session, title=title, description=flag, status=Status.MUMBLE)
            post_id = created_request["request"]["id"]

        self.cquit(Status.OK, f"{email}", f'{email}:{password}:{post_id}')

    def get(self, flag_id: str, flag: str, vuln: str):
        session = self.get_initialized_session()
        email, password, request_id = flag_id.split(':')
        request_id = int(request_id)
        self.mch.login(session, email, password, Status.CORRUPT)
        data = self.mch.get_request(session, request_id=request_id, status=Status.CORRUPT)
        if vuln == "1":
            self.assert_eq(data["description"], flag, "Description value is invalid (flag was not found)", Status.CORRUPT)
        self.cquit(Status.OK)
        # check that flag is still in description after some time

if __name__ == '__main__':
    c = Checker(sys.argv[2])
    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
