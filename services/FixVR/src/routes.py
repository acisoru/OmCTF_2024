from aiohttp import web
from handlers import *

def setup_routes(app):
    app.router.add_route('POST', '/register', register)
    app.router.add_route('POST', '/login', login)
    app.router.add_route('POST', '/api/edit-request/{requestId}', edit_request)
    app.router.add_route('POST', '/api/create-request', create_request)
    app.router.add_route('POST', '/api/delete-request/{requestId}', delete_request)
    app.router.add_route('POST', '/api/change-password', change_password)
    app.router.add_route('GET', '/api/requests', get_requests)
    app.router.add_route('GET', '/api/profile', profile)
    
    app.router.add_static('/static/', path='./static', name='static', follow_symlinks=True)
    app.router.add_route('GET', '/', index_page)
    app.router.add_route('GET', '/panel', panel_page)
    app.router.add_route('GET', '/profile', profile_page)
    app.router.add_route('GET', '/registration', registration_page)
    app.router.add_route('GET', '/login', login_page)
