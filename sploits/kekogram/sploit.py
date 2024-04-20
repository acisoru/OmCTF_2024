import sys
import json

import gmpy2

from checklib import *

from cipher import MyCipher
from Crypto.Util.Padding import unpad
from kekogram_lib import CheckMachine

HOST = sys.argv[1]
HINT = sys.argv[2]

def main():
    hint = json.loads(HINT)
    c = CheckMachine(BaseChecker(HOST))
    with c.connect() as sock:
        members = c.get_chat_members(sock, hint["chat"].encode(), Status.MUMBLE)
        print(members)
        enc_master_key = c.get_master_key(sock, hint["chat"].encode(), members[0], Status.MUMBLE)
        message = c.get_message(sock, hint["chat"].encode(), hint["message"].encode(), Status.MUMBLE)

        key_int = int(gmpy2.iroot(enc_master_key, 3)[0])
        assert 16 * 8 >= key_int.bit_length()

        key = key_int.to_bytes(16, byteorder='little')

        cipher = MyCipher(key)
        print(unpad(cipher.decrypt(message.data), 16), flush=True)


if __name__ == "__main__":
    main()
