import asyncio
from aiohttp import web
from routes import setup_routes
from db import initialize_db
from cryptography import fernet
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import base64


CIPHER_KEY = b'\xbe\x08\xc1B\xbe\xbb\x19\xe1\xa02\xe2A\xcb\x8a\xce\x95\x87\xd5\x80g\xe3\xd4U5P\x07\x86D\x9d\xa0\xde\xb1'

app = web.Application(middlewares=[session_middleware(EncryptedCookieStorage(CIPHER_KEY))])
setup_routes(app)

asyncio.run(initialize_db())
web.run_app(app, port=8080)
