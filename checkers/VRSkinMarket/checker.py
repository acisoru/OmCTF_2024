#!/usr/bin/env python3

import sys
import requests

from checklib import *
from shop_checker_lib import *


PORT=8080

class Checker(BaseChecker):
    vulns: int = 2
    timeout: int = 10
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except self.get_check_finished_exception():
            raise
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')
        except Exception as e:
            self.cquit(Status.ERROR, f"{e}", e)

    def check(self): 
        #create user1 and check add_merch
        with CheckMachine(self.host, port=PORT) as c:
            user1 = CheckMachine.generate_user()
            resp = c.register(user1)
            self.assert_eq(resp.status_code, 201, "Can't register")
            resp = c.login(user1)
            self.assert_eq(resp.status_code, 200, "Can't login")
            resp = c.add_merch(sent_data:=CheckMachine.generate_merch())
            merch_id = resp.json()["ID"]
            self.assert_eq(resp.status_code, 201, "Can't add merchandise")
            resp = c.get_my_merch(merch_id).json()
            self.assert_eq(Merch(resp["name"], resp["description"], resp["price"], resp["NFTToken"], resp["picture"]) == sent_data, True, "Added and recieved merch are different")
            self.assert_eq(resp["NFTToken"] == sent_data.NFTToken, True, "Added and recieved merch are different")           
        #create user2 and check buy_merch
        with CheckMachine(self.host, port=PORT) as c: 
            user2 = CheckMachine.generate_user()
            resp = c.register(user2)
            user2_id = resp.json()["ID"]
            self.assert_eq(resp.status_code, 201, "Can't register")
            resp = c.login(user2)
            self.assert_eq(resp.status_code, 200, "Can't login")
            resp = c.get_profile()
            self.assert_eq(resp.status_code, 200, "Can't get profile")
            self.assert_eq(resp.json()["ID"], user2_id, "Wrong profile")
            self.assert_eq(resp.json()["flag"], 'No flag here!', "Flag deleted!")
            resp = c.add_to_cart(merch_id)
            if resp.status_code != 200:
                resp = c.get_merch(merch_id)
                self.assert_eq(resp.status_code, 200, "can't add to cart")
                self.assert_in_list_dicts([{1 :"ordered"}, {1: "bought"}], 1, resp.json()["status"], "can't add to cart")            
            resp = c.get_cart()
            self.assert_eq(resp.status_code, 200, "can't get cart")
            cart_merch = resp.json()['goods'][0]
            self.assert_eq(Merch(cart_merch["name"], cart_merch["description"], cart_merch["price"], cart_merch["NFTToken"], cart_merch["picture"]) == sent_data, True, "Added and recieved merch are different")
            resp = c.create_order(resp.json()["ID"])
            self.assert_eq(resp.status_code, 201, "can't create order")
            resp = c.get_order(resp.json()["ID"])
            order_merch = resp.json()['cart']['goods'][0]
            self.assert_eq(Merch(order_merch["name"], order_merch["description"], order_merch["price"], order_merch["NFTToken"], order_merch["picture"]) == sent_data, True, "Added and recieved merch are different")
            buy_merch = c.buy({"order" : resp.json()["ID"], "cart" : {"price" : resp.json()['cart']['price']}})
            self.assert_eq(buy_merch.status_code, 400, "Can't buy")
            self.assert_eq(buy_merch.json()["err"].startswith("Bad Request: not enough"), True, "Can't buy")
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: int):
        with CheckMachine(self.host, port=PORT) as c:
            if vuln == '1':
                user = CheckMachine.generate_user(flag=flag)
                resp = c.register(user)
                self.assert_eq(resp.status_code, 201, "Can't register")
                self.cquit(Status.OK, user.username, f'{user.username}:{user.password}')
            user = CheckMachine.generate_user()
            resp = c.register(user)
            self.assert_eq(resp.status_code, 201, "Can't register")
            resp = c.login(user)
            self.assert_eq(resp.status_code, 200, "Can't login")
            resp = c.add_merch(sent_data:=CheckMachine.generate_merch(flag=flag))
            self.assert_eq(resp.status_code, 201, "Can't add merch")
            self.cquit(Status.OK, resp.json()["ID"], f'{user.username}:{user.password}:{resp.json()["ID"]}')

    def get(self, flag_id: str, flag: str, vuln: str):
        with CheckMachine(self.host, port=PORT) as c:
            args = flag_id.split(':')
            if len(args) == 2:
                resp = c.login(User(args[0], args[1]))
                self.assert_eq(resp.status_code, 200, "Can't login", status=Status.CORRUPT)
                resp = c.get_profile()
                self.assert_eq(200, resp.status_code, "Can't get profile", Status.CORRUPT)  
                self.assert_eq(flag, resp.json()["flag"], "profile value is invalid", Status.CORRUPT)
                self.cquit(Status.OK)
            resp = c.login(User(args[0], args[1]))
            self.assert_eq(resp.status_code, 200, "Can't login", status=Status.CORRUPT)
            resp = c.get_my_merch(args[2])
            self.assert_eq(200, resp.status_code, "Can't get profile", Status.CORRUPT)
            self.assert_eq(flag, resp.json()["NFTToken"], "merchandise value is invalid", Status.CORRUPT)
        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
    