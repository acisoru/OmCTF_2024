#!/usr/bin/env python3
import sys
import os
import requests
import random
import uuid

from checklib import *
from clone_marketlib import *
from pathlib import Path

BASE_DIR = Path(__file__).absolute().resolve().parent

class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 5
    uses_attack_data: bool = False

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
        username, password = rnd_username(), rnd_password() 

        cloneUUID = str(uuid.uuid4())
        description = rnd_string(20)

        self.mch.signup(session, username, password, Status.MUMBLE)
        self.mch.signin(session, username, password, Status.MUMBLE)

        self.mch.createclone(session, cloneUUID=cloneUUID, description=description, status=Status.MUMBLE)
        self.mch.createclonefromurl(session, "http://127.0.0.1:8080/test.txt", status=Status.MUMBLE)

        data = self.mch.getclones(session, user_id=session.cookies.get_dict()["id"], status=Status.MUMBLE)
        data = data["clones"]
        self.mch.signout(session, status=Status.MUMBLE)

        self.assert_eq(next((request for request in data if request['cloneUUID'] == cloneUUID), None), {"cloneUUID": cloneUUID, "description": description}, "Return data is invalid", Status.CORRUPT)
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        session = self.get_initialized_session()
        username, password = rnd_username(), rnd_password() 
        self.mch.signup(session, username, password, Status.MUMBLE)
        self.mch.signin(session, username, password, Status.MUMBLE)
        cloneUUIDflag = str(uuid.uuid4())
        if vuln == "1":
            for i in range(random.randint(1, 4)):
                cloneUUID = str(uuid.uuid4())
                description = rnd_string(20)
                self.mch.createclone(session, cloneUUID=cloneUUID, description=description, status=Status.MUMBLE)
            self.mch.createclone(session, cloneUUID=cloneUUIDflag, description=flag, status=Status.MUMBLE)

        self.cquit(Status.OK, f'{username}:{password}:{cloneUUIDflag}')

    def get(self, flag_id: str, flag: str, vuln: str):
        session = self.get_initialized_session()
        username, password, cloneUUID = flag_id.split(':')
        self.mch.signin(session, username, password, Status.CORRUPT)
        data = self.mch.getclones(session, user_id=session.cookies.get_dict()["id"], status=Status.MUMBLE)
        data = data["clones"]
        if vuln == "1":
            self.assert_eq(next((request for request in data if request['cloneUUID'] == cloneUUID), None), {"cloneUUID": cloneUUID, "description": flag}, "Description value is invalid (flag was not found)", Status.CORRUPT)
        self.cquit(Status.OK)

if __name__ == '__main__':
    c = Checker(sys.argv[2])
    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)