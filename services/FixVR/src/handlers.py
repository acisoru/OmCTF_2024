from aiohttp import web
import aiosqlite
from aiohttp import web
from cryptography import fernet
from functools import wraps
import aiosqlite
from aiohttp_session import get_session
import hashlib
import logging
from db import DB_NAME


logging.basicConfig(level=logging.INFO)

def require_login(func):
    @wraps(func)
    async def wrapper(request):
        session = await get_session(request)
        if 'user' in session:
            return await func(request)
        else:
            return web.HTTPFound('/login')

    return wrapper

async def index_page(request):
    return web.FileResponse('./html/index.html')

async def login_page(request):
    return web.FileResponse('./html/login.html')

@require_login
async def panel_page(request):
    return web.FileResponse('./html/panel.html')

@require_login
async def profile_page(request):
    return web.FileResponse('./html/profile.html')

async def registration_page(request):
    return web.FileResponse('./html/registration.html')


async def register(request):
    data = await request.post()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return web.json_response({'message': 'Email or password is missing'}, status=400)

    if len(email) > 100:
        return web.json_response({'message': 'Email exceeds maximum length'}, status=400)
        
    password = hashlib.sha256(password.encode()).hexdigest()

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()
            await cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            await db.commit()
    except Exception as e:
        return web.json_response({'message': 'Error: {}'.format(str(e))}, status=500)

    session = await get_session(request)
    session['user'] = email

    raise web.HTTPFound('/panel')


async def login(request):
    data = await request.post()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return web.json_response({'message': 'Email or password is missing'}, status=400)

    password = hashlib.sha256(password.encode()).hexdigest()

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()
            await cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = await cursor.fetchone()
    except Exception as e:
        return web.json_response({'message': 'Error: {}'.format(str(e))}, status=500)

    if user:
        session = await get_session(request)
        session['user'] = email
        return web.json_response({'message': 'Logged in successfully', 'redirect': '/panel'})
    else:
        return web.json_response({'message': 'Invalid email or password'}, status=400)


@require_login
async def edit_request(request):
    data = await request.json()
    requestId = request.match_info['requestId']
    title = data.get('title')
    description = data.get('description')

    if not requestId:
        return web.json_response({'message': 'Request ID is missing'}, status=400)

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()

            fields_to_update = []
            values = []
            if title is not None:
                if len(title) > 256:
                    return web.json_response({'message': 'Title exceeds maximum length'}, status=400)
                fields_to_update.append('title = ?')
                values.append(title)
            if description is not None:
                if len(description) > 256:
                        return web.json_response({'message': 'Description exceeds maximum length'}, status=400)
                fields_to_update.append('description = ?')
                values.append(description)

            values.append(requestId)

            sql = 'UPDATE requests SET {} WHERE id = ?'.format(', '.join(fields_to_update))

            await cursor.execute(sql, values)
            await db.commit()

            await cursor.execute('SELECT title, description FROM requests WHERE id = ?', (requestId,))
            updated_request = await cursor.fetchone()
    except Exception as e:
        return web.json_response({'message': 'Error while editing request'}, status=500)

    return web.json_response({
        'message': 'Request edited successfully',
        'request': {
            'title': updated_request[0],
            'description': updated_request[1]
        }
    })

@require_login
async def create_request(request):
    data = await request.json()
    title = data.get('title')
    description = data.get('description')
    session = await get_session(request)
    user = session.get('user')

    if not title or not description:
        return web.json_response({'message': 'Title or description is missing'}, status=400)

    if len(title) > 256:
        return web.json_response({'message': 'Title exceeds maximum length'}, status=400)
    if len(description) > 256:
        return web.json_response({'message': 'Description exceeds maximum length'}, status=400)


    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()
            await cursor.execute('INSERT INTO requests (title, description, user_id) VALUES (?, ?, (SELECT id FROM users WHERE email = ?))', (title, description, user))
            request_id = cursor.lastrowid
            await db.commit()
    except Exception as e:
        return web.json_response({'message': 'Error while creating request'}, status=500)

    return web.json_response({'message': 'Request created successfully', 'request': {'id': request_id, 'title': title, 'description': description}})


@require_login
async def delete_request(request):
    requestId = request.match_info.get('requestId')

    if not requestId:
        return web.json_response({'message': 'Request ID is missing'}, status=400)

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()
            await cursor.execute('DELETE FROM requests WHERE id = ?', (requestId,))
            await db.commit()
    except Exception as e:
        return web.json_response({'message': 'Error while deleting request'}, status=500)

    return web.json_response({'message': 'Request deleted successfully'})


@require_login
async def get_requests(request):
    session = await get_session(request)
    user = session.get('user')

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()
            await cursor.execute('''
                SELECT * FROM (
                    SELECT * FROM requests 
                    WHERE user_id = (SELECT id FROM users WHERE email = ?)
                    ORDER BY id DESC LIMIT 50
                ) ORDER BY id ASC
            ''', (user,))

            requests = await cursor.fetchall()
    except Exception as e:
        return web.json_response({'message': 'Error while getting requests'}, status=500)

    requests = [dict(zip([column[0] for column in cursor.description], row)) for row in requests]
    return web.json_response(requests)

@require_login
async def change_password(request):
    data = await request.post()
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    session = await get_session(request)
    user = session.get('user')

    if not current_password or not new_password:
        return web.json_response({'message': 'Current or new password is missing'}, status=400)

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()

            await cursor.execute('SELECT password FROM users WHERE email = ?', (user,))
            stored_password_hash = await cursor.fetchone()
            current_password_hash = hashlib.sha256(current_password.encode()).hexdigest()
            if stored_password_hash[0] != current_password_hash:
                return web.Response(status=403)

            new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            await cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password_hash, user))
            await db.commit()
    except Exception as e:
        return web.json_response({'message': 'Error while changing password'}, status=500)

    return web.Response(status=200)


@require_login 
async def profile(request):
    session = await get_session(request)
    user = session.get('user')

    if not user:
        return web.json_response({'message': 'Not logged in'}, status=403)

    try:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.cursor()

            await cursor.execute('SELECT email FROM users WHERE email = ?', (user,))
            user_data = await cursor.fetchone()

            await cursor.execute('SELECT COUNT(*) FROM requests WHERE user_id = (SELECT id FROM users WHERE email = ?)', (user,))
            request_count = await cursor.fetchone()
    except Exception as e:
        return web.json_response({'message': 'Error while fetching user profile'}, status=500)
        
    profile_data = {
        'email': user_data[0],
        'request_count': request_count[0]
    }

    return web.json_response(profile_data)
