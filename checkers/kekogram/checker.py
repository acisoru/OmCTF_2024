#!/usr/bin/env python3

import random
import secrets
import sys
import uuid
import json

from checklib import *
from cipher import MyCipher
from Crypto.Util.Padding import unpad

from kekogram_lib import CheckMachine


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 15
    uses_attack_data: bool = True
    c: CheckMachine

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.c = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except self.get_check_finished_exception():
            raise
        except ConnectionRefusedError:
            self.cquit(Status.DOWN, "Connection refused", "Connection refused")

        except Exception as e:
            self.cquit(Status.DOWN, "internal checker error", f"internal checker error {e}")

    def check(self):
        with self.c.connect() as sock:
            username1 = rnd_username()
            user1 = self.c.register(sock, username1.encode(), Status.MUMBLE)

            username2 = rnd_username()
            user2 = self.c.register(sock, username2.encode(), Status.MUMBLE)

            chat_id = rnd_string(16)
            self.c.make_chat(sock, chat_id.encode(), [username1.encode(), username2.encode()], Status.MUMBLE)

            data = rnd_string(16)
            challenge = self.c.get_challenge(sock, Status.MUMBLE)
            message_id = self.c.put_message(sock,
                                            chat_id=chat_id.encode(),
                                            username=username1.encode(),
                                            challenge=pow(int.from_bytes(challenge, 'little'), user1.d, user1.n),
                                            message=data.encode(), 
                                            status=Status.MUMBLE,
                                            ).decode()


            encrypted_master_key = self.c.get_master_key(sock, chat_id.encode(), username2.encode(), Status.MUMBLE)

            master_key_int = pow(encrypted_master_key, user2.d, user2.n)
            self.assert_gte(16 * 8, master_key_int.bit_length(), "invalid key", Status.MUMBLE)
            master_key = master_key_int.to_bytes(16, 'little')


            message = self.c.get_message(sock, chat_id.encode(), message_id.encode(), Status.MUMBLE)

            cipher = MyCipher(master_key)
            service_data = unpad(cipher.decrypt(message.data), 16)

            self.assert_eq(service_data, data.encode(), "incorrect flag", Status.MUMBLE)


            self.c.exit(sock, Status.MUMBLE)
            self.cquit(Status.OK)


    def put(self, flag_id: str, flag: str, vuln: str):
        with self.c.connect() as sock:
            username1 = rnd_username()
            user1 = self.c.register(sock, username1.encode(), Status.MUMBLE)

            username2 = rnd_username()
            user2 = self.c.register(sock, username2.encode(), Status.MUMBLE)

            chat_id = rnd_string(16)
            self.c.make_chat(sock, chat_id.encode(), [username1.encode(), username2.encode()], Status.MUMBLE)

            challenge = self.c.get_challenge(sock, Status.MUMBLE)
            message_id = self.c.put_message(sock,
                                            chat_id=chat_id.encode(),
                                            username=username1.encode(),
                                            challenge=pow(int.from_bytes(challenge, 'little'), user1.d, user1.n),
                                            message=flag.encode(), 
                                            status=Status.MUMBLE,
                                            ).decode()
            self.c.exit(sock, Status.MUMBLE)
            self.cquit(Status.OK, 
                       json.dumps({
                           "chat": chat_id,
                           "message": message_id,
                       }),
                       json.dumps({
                           "chat": chat_id,
                           "message": message_id,
                           "user": username2,
                           "d": user2.d,
                       }),
                       )


    def get(self, flag_id: str, flag: str, vuln: str):
        with self.c.connect() as sock:
            flag_id = json.loads(flag_id)

            user2 = self.c.get_user_public_key(sock, flag_id["user"].encode(), Status.CORRUPT)

            encrypted_master_key = self.c.get_master_key(sock, flag_id["chat"].encode(), flag_id["user"].encode(), Status.MUMBLE)

            master_key_int = pow(encrypted_master_key, flag_id["d"], user2.n)
            self.assert_gte(16 * 8, master_key_int.bit_length(), "invalid key", Status.CORRUPT)
            master_key = master_key_int.to_bytes(16, 'little')


            message = self.c.get_message(sock, flag_id["chat"].encode(), flag_id["message"].encode(), Status.CORRUPT)

            cipher = MyCipher(master_key)
            service_flag = unpad(cipher.decrypt(message.data), 16)

            self.assert_eq(service_flag, flag.encode(), "incorrect flag", Status.CORRUPT)

            self.c.exit(sock, Status.MUMBLE)
            self.cquit(Status.OK)



if __name__ == "__main__":
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
