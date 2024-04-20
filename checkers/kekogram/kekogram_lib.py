import random
import string
import struct
from typing import List, NamedTuple

from checklib import *
import socket

from cipher import MyCipher

LIST_CHATS = 1
LIST_MESSAGES = 2
GET_MESSAGE = 3
PUT_MESSAGE = 4
REGISTER = 5
GET_CHALLENGE = 6
GET_USER_PUBLIC_KEY = 7
GET_MASTER_KEY = 8
MAKE_CHAT = 9
GET_CHAT_MEMBERS = 10
EXIT = 100

DIFFIE_HELMAN_P = 166727477384293939242219142227789530796466329208849443901802611959943352892249771607230820568414678992079501342693735648764558563698109613819330211099628000262913488679290287909809436901051629590870452352871567920731552217919941040875588300788905763303194409992090519537202043666542027124394302408863329705689
DIFFIE_HELMAN_G = 31337
PORT = 2112

class GetMessageResponse(NamedTuple):
    username: bytes
    data: bytes

class RegisterResponse(NamedTuple):
    n: int
    e: int
    d: int

class GetUserPublicKeyResponse(NamedTuple):
    n: int
    e: int

class CheckMachine:
    c: BaseChecker
    sock: socket.socket
    aes_key: bytes

    def __init__(self, c: BaseChecker):
        self.c = c

    # def __init__(self, host: string):
    #     # self.sock = socket.socket()
    #     # self.sock.connect(host, PORT)
    #     # self._diffie_helman()
    #     # self.sock = process("./kekogram")
    #     self.sock = process("./kekogram 2>log", shell=True)
    #     # print(self.sock.recv(4))
    #     # 1/0

    def connect(self):
        sock = socket.socket()
        sock.connect((self.c.host, PORT))
        # sock = process("./kekogram 2>log", shell=True)
        self._diffie_helman(sock)
        return sock

    def _diffie_helman(self, sock: socket.socket):

        my_power = random.randint(0, DIFFIE_HELMAN_P - 1)
        my_g = pow(DIFFIE_HELMAN_G, my_power, DIFFIE_HELMAN_P)

        sock.send(self.marshal_long(my_g))

        l = struct.unpack("<I", self.recvall(sock, 4))[0]
        other_g = int.from_bytes(self.recvall(sock, l), byteorder='little')

        key_g = pow(other_g, my_power, DIFFIE_HELMAN_P)

        self.cipher_key = key_g.to_bytes((key_g.bit_length() + 7) // 8, byteorder='little')[:16]
        self.cipher = MyCipher(self.cipher_key)

    @staticmethod
    def recvall(sock: socket.socket, n: int) -> bytes:
        res = b''

        while len(res) < n:
            res += sock.recv(n - len(res))
        return res

    @classmethod
    def marshal_int(cls, n: int) -> bytes:
        return struct.pack("<I", n)

    @classmethod
    def marshal_bytes(cls, b: bytes) -> bytes:
        return cls.marshal_int(len(b)) + b

    @classmethod
    def marshal_long(cls, n: int) -> bytes:
        return cls.marshal_bytes(n.to_bytes(
            length=(n.bit_length() + 7) // 8, 
            byteorder='little',
        ))

    def unmarshal_int(self, b: bytes, status: Status) -> (int, bytes):
        self.c.assert_gte(len(b), 4, f"ran out of data", status)
        return struct.unpack("<I", b[:4])[0], b[4:]

    def unmarshal_bytes(self, b: bytes, status: Status) -> (bytes, bytes):
        self.c.assert_gte(len(b),  4 , f"ran out of data", status)
        l = struct.unpack("<I", b[:4])[0]
        self.c.assert_gte(len(b), 4 + l, f"ran out of data", status)

        return b[4:l + 4], b[l + 4:]

    def unmarshal_long(self, b: bytes, status: Status) -> (int, bytes):
        data, rem = self.unmarshal_bytes(b, status)
        return int.from_bytes(data, byteorder='little'), rem
    
    def read_packet(self, sock: socket.socket, status: Status) -> bytes:
        l = struct.unpack("<I", self.recvall(sock, 4))[0]
        encrypted = self.recvall(sock, l)
        assert len(encrypted) % 16 == 0

        data = self.cipher.decrypt(encrypted)

        if data[0] != 0:
            self.c.cquit(status, f"got error {data[1:]}", f"got error {data[1:]}")

        return data[1:]

    def write_packet(self, sock: socket.socket, data: bytes):
        data += bytes([16 - len(data) % 16]) * (16 - len(data) % 16)
        assert len(data) % 16 == 0

        sock.send(struct.pack("<I", len(data)))
        sock.send(self.cipher.encrypt(data))

    def register(self, sock: socket.socket, username: bytes, status: Status) -> RegisterResponse:
        self.write_packet(sock, bytes([REGISTER]) + self.marshal_bytes(username))

        rem = self.read_packet(sock, status)
        n, rem = self.unmarshal_long(rem, status)
        e, rem = self.unmarshal_long(rem, status)
        d, rem = self.unmarshal_long(rem, status)

        return RegisterResponse(
            n=n,
            e=e,
            d=d,
        )

    def put_message(self, sock: socket.socket, chat_id: bytes, username: bytes, message: bytes, challenge: int, status: Status) -> bytes:
        self.write_packet(sock, bytes([PUT_MESSAGE]) + self.marshal_bytes(chat_id) + self.marshal_bytes(username) + self.marshal_long(challenge) + self.marshal_bytes(message))

        rem = self.read_packet(sock, status)
        message_id, rem = self.unmarshal_bytes(rem, status)

        return message_id

    def get_message(self, sock: socket.socket, chat_id: bytes, message_id: bytes, status: Status) -> GetMessageResponse:
        self.write_packet(sock, bytes([GET_MESSAGE]) + self.marshal_bytes(chat_id) + self.marshal_bytes(message_id))

        rem = self.read_packet(sock, status)
        username, rem = self.unmarshal_bytes(rem, status)
        data, rem = self.unmarshal_bytes(rem, status)

        return GetMessageResponse(
            username=username,
            data=data,
        )

    def get_user_public_key(self, sock: socket.socket, username: bytes, status: Status) -> GetUserPublicKeyResponse:
        self.write_packet(sock, bytes([GET_USER_PUBLIC_KEY]) + self.marshal_bytes(username))

        rem = self.read_packet(sock, status)
        n, rem = self.unmarshal_long(rem, status)
        e, rem = self.unmarshal_long(rem, status)

        return GetUserPublicKeyResponse(
            n=n,
            e=e,
        )

    def make_chat(self, sock: socket.socket, chat_id: bytes, members: List[bytes], status: Status):
        self.write_packet(sock, bytes([MAKE_CHAT]) + self.marshal_bytes(chat_id) + self.marshal_int(len(members)) + b''.join(self.marshal_bytes(m) for m in members))

        rem = self.read_packet(sock, status)


    def get_master_key(self, sock: socket.socket, chat_id: bytes, username: bytes, status: Status) -> int:
        self.write_packet(sock, bytes([GET_MASTER_KEY]) + self.marshal_bytes(chat_id) + self.marshal_bytes(username))

        rem = self.read_packet(sock, status)
        n, rem = self.unmarshal_long(rem, status)

        return n

    def get_challenge(self, sock: socket.socket, status: Status) -> bytes:
        self.write_packet(sock, bytes([GET_CHALLENGE]))

        rem = self.read_packet(sock, status)
        challenge, rem = self.unmarshal_bytes(rem, status)

        return challenge

    def list_messages(self, sock: socket.socket, chat_id: bytes, status: Status) -> List[bytes]:
        self.write_packet(sock, bytes([LIST_MESSAGES]) + self.marshal_bytes(chat_id))

        rem = self.read_packet(sock, status)
        res = []
        n, rem = self.unmarshal_int(rem, status)
        for _ in range(n):
            m_id, rem = self.unmarshal_bytes(rem, status)
            res.append(m_id)

        return res

    def list_chats(self, sock: socket.socket, status: Status) -> List[bytes]:
        self.write_packet(sock, bytes([LIST_CHATS]))

        rem = self.read_packet(sock, status)
        res = []
        n, rem = self.unmarshal_int(rem, status)
        for _ in range(n):
            uname, rem = self.unmarshal_bytes(rem, status)
            res.append(uname)

        return res

    def get_chat_members(self, sock: socket.socket, chat_id: bytes, status: Status) -> List[bytes]:
        self.write_packet(sock, bytes([GET_CHAT_MEMBERS]) + self.marshal_bytes(chat_id))

        rem = self.read_packet(sock, status)
        res = []
        n, rem = self.unmarshal_int(rem, status)
        for _ in range(n):
            m_id, rem = self.unmarshal_bytes(rem, status)
            res.append(m_id)

        return res

    def exit(self, sock: socket.socket, status: Status) -> List[bytes]:
        self.write_packet(sock, bytes([EXIT]))
