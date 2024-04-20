from flask import Flask, jsonify, request
import grpc
import clone_market_pb2
import clone_market_pb2_grpc
import uuid
import json
from flask import render_template

app = Flask(__name__)

def get_grpc_client():
    channel = grpc.insecure_channel('grpc_server:50051')
    stub = clone_market_pb2_grpc.CloneMarketStub(channel)
    return stub

def is_valid_uuid(uuid_string):
    if not isinstance(uuid_string, str):
        print(uuid_string)
        return False
    try:
        print(uuid_string)
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False

def is_simple_string(value):
    if not isinstance(value, str):
        return False
    try:
        json.loads(value)
        return False
    except json.JSONDecodeError:
        return True


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        data = request.get_json()
        pong = data.get('pong', '')

        client = get_grpc_client()
        ping_request = clone_market_pb2.PingRequest(pong=pong)
        ping_response = client.Ping(ping_request)

        return jsonify({'pong': ping_response.pong})
    else:
        return render_template('ping.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        client = get_grpc_client()
        signup_request = clone_market_pb2.SignUpRequest(username=username, password=password)

        try:
            signup_response = client.SignUp(signup_request)
            response_data = {
                'id': signup_response.id,
                'server_resp': signup_response.server_resp
            }
            return jsonify(response_data), 200

        except grpc.RpcError as e:
            error_message = f"gRPC error: {e.details()}"
            return jsonify({'error': error_message}), 500
    else:
        return render_template('signup.html')
    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        client = get_grpc_client()
        signin_request = clone_market_pb2.SignInRequest(username=username, password=password)

        try:
            signin_response = client.SignIn(signin_request)
            if signin_response.id != -1:
                response_data = {
                    'id': signin_response.id,
                    'token': signin_response.token
                }
                return jsonify(response_data), 200
            else:
                return jsonify({'error': 'Invalid username or password'}), 401

        except grpc.RpcError as e:
            error_message = f"gRPC error: {e.details()}"
            return jsonify({'error': error_message}), 500
    else:
        return render_template('signin.html')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('id')
        token = data.get('token')

        client = get_grpc_client()
        signout_request = clone_market_pb2.SignOutRequest(id=user_id, token=token)

        try:
            signout_response = client.SignOut(signout_request)
            response_data = {
                'success': signout_response.success,
                'server_resp': signout_response.server_resp
            }
            return jsonify(response_data), 200

        except grpc.RpcError as e:
            error_message = f"gRPC error: {e.details()}"
            return jsonify({'error': error_message}), 500
    else:
        return render_template('signout.html')
    

@app.route('/createclone', methods=['GET', 'POST'])
def create_clone():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('id')
        token = data.get('token')
        clone_uuid = data.get('cloneUUID')
        description = data.get('description')

        if not isinstance(user_id, int):
            return jsonify({'error': 'Invalid user ID'}), 400

        if not isinstance(token, str):
            return jsonify({'error': 'Invalid token'}), 400

        if not is_valid_uuid(clone_uuid):
            return jsonify({'error': 'Invalid cloneUUID'}), 400
        
        if not is_simple_string(description):
            return jsonify({'error': 'Invalid description. It must be a simple string without JSON structure.'}), 400

        client = get_grpc_client()
        create_clone_request = clone_market_pb2.CreateCloneRequest(
            id=user_id,
            token=token,
            cloneUUID=clone_uuid,
            description=description
        )

        try:
            create_clone_response = client.CreateClone(create_clone_request)
            response_data = {
                'success': create_clone_response.success,
                'server_resp': create_clone_response.server_resp
            }
            return jsonify(response_data), 200

        except grpc.RpcError as e:
            error_message = f"gRPC error: {e.details()}"
            return jsonify({'error': error_message}), 500
    else:
        return render_template('createclone.html')
    
@app.route('/getclones', methods=['GET', 'POST'])
def get_clones():
    if request.method == 'POST':
        data = request.get_json()
        my_id = data.get('my_id')
        user_id = data.get('user_id')
        token = data.get('token')

        if not isinstance(my_id, int):
            return jsonify({'error': 'Invalid my_id'}), 400

        if not isinstance(user_id, int):
            return jsonify({'error': 'Invalid user_id'}), 400

        if not isinstance(token, str):
            return jsonify({'error': 'Invalid token'}), 400

        client = get_grpc_client()
        get_clones_request = clone_market_pb2.GetClonesRequest(
            my_id=my_id,
            user_id=user_id,
            token=token
        )

        try:
            get_clones_response = client.GetClones(get_clones_request)
            clones = []
            for clone_info in get_clones_response.clones:
                clone_data = json.loads(clone_info)
                clones.append({
                    'cloneUUID': clone_data['cloneuuid'],
                    'description': clone_data['description']
                })
            response_data = {
                'clones': clones
            }
            return jsonify(response_data), 200

        except grpc.RpcError as e:
            status_code = e.code()
            if status_code == grpc.StatusCode.UNAUTHENTICATED:
                return jsonify({'error': 'User not logged in'}), 401
            elif status_code == grpc.StatusCode.NOT_FOUND:
                return jsonify({'error': 'User not found'}), 404
            elif status_code == grpc.StatusCode.PERMISSION_DENIED:
                return jsonify({'error': 'User does not have permission to access the requested clones'}), 403
            else:
                error_message = f"gRPC error: {e.details()}"
                return jsonify({'error': error_message}), 500

    else:
        return render_template('getclones.html')


@app.route('/createclonefromurl', methods=['GET', 'POST'])
def create_clone_from_url():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('id')
        token = data.get('token')
        url = data.get('url')

        if not isinstance(user_id, int):
            return jsonify({'error': 'Invalid user ID'}), 400

        if not isinstance(token, str):
            return jsonify({'error': 'Invalid token'}), 400

        if not isinstance(url, str):
            return jsonify({'error': 'Invalid URL'}), 400

        client = get_grpc_client()
        create_clone_from_url_request = clone_market_pb2.CreateCloneFromURLRequest(
            id=user_id,
            token=token,
            url=url
        )

        try:
            create_clone_from_url_response = client.CreateCloneFromURL(create_clone_from_url_request)
            response_data = {
                'success': create_clone_from_url_response.success,
                'server_resp': create_clone_from_url_response.server_resp
            }
            return jsonify(response_data), 200

        except grpc.RpcError as e:
            status_code = e.code()
            if status_code == grpc.StatusCode.UNAUTHENTICATED:
                return jsonify({'error': 'User not logged in'}), 401
            elif status_code == grpc.StatusCode.NOT_FOUND:
                return jsonify({'error': 'User not found'}), 404
            else:
                error_message = f"gRPC error: {e.details()}"
                return jsonify({'error': error_message}), 500
    else:
        return render_template('createclonefromurl.html')

@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html')


if __name__ == '__main__':
    app.run()