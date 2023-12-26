from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt_identity
import sqlite3


## REGISTER MODEL
class Register(Resource):
    def post(self):
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        email = data.get('email')

        
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM users WHERE username = ? AND role = ?', (username, role))
        existing_user = cursor1.fetchone()

        if existing_user:
            conn1.close()
            return jsonify({'message': 'Username already exists'}), 400

        # Insert the user data into the database
        cursor1.execute('INSERT INTO users (first_name, last_name, username, password, role, email) VALUES (?, ?, ?, ?, ?, ?)', (first_name, last_name, username, password, role, email))
        conn1.commit()


        user_info = verify_user_credentials(username, password, role)

        if user_info:
            access_token = create_access_token(identity=user_info[0])
            refresh_token = create_refresh_token(identity=user_info[0])

            return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
        else:
            return jsonify({'message': 'Invalid credentials'})

## ADMIN LOGIN MODEL 
class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        admin_info = verify_user_credentials(username, password, 'admin')

        if admin_info:
            access_token = create_access_token(identity=admin_info[0])
            return {'message': 'Login successful', 'access_token': access_token}
        
        return {'message': 'Invalid credentials'}, 401


## USER LOGIN MODEL 
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user_info = verify_user_credentials(username, password, 'user')

        if user_info:
            access_token = create_access_token(identity=user_info[0])
            return {'message': 'Login successful', 'access_token': access_token}
        
        return {'message': 'Invalid credentials'}, 401
    

## MANAGER LOGIN MODEL 
class ManagerLoginRequest(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        manager_info = verify_user_credentials(username, password, 'manager')
        token = create_access_token(identity=manager_info[0])

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT first_name, last_name FROM users WHERE username = ? AND password = ? AND role = ?', (username, password, 'manager'))
        name = cursor1.fetchone()

        cursor1.execute('SELECT * FROM login_requests WHERE username = ? AND password = ?', (username, password))
        req = cursor1.fetchone()

        if manager_info:
            if req is not None:
                return {'message': req, 'access_token': token}
            else:
                cursor1.execute('INSERT INTO login_requests (first_name, last_name, username, password, token, approved, status) VALUES (?, ?, ?, ?, ?, 0, ?)', (name[0], name[1], username, password, token, "Pending"))
                conn1.commit()
                return {'message': 'Login request submitted for approval', 'access_token': token}

        conn1.close()
        return {'message': 'Invalid credentials'}, 401

## MANAGER LOGIN REQUEST MODEL 
class LoginRequests(Resource):
    def get(self):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM login_requests')
        requests = cursor1.fetchall()

        login_requests = [{'id': row[0], 'first_name': row[1], 'last_name': row[2], 'username': row[3], 'password': row[4], 'token': row[5], 'approved': row[6], 'status': row[7]} for row in requests]
        return {'login_requests': login_requests}

 ## APPROVE MANAGER LOGIN REQUEST MODEL    
class ApproveLoginRequest(Resource):
    def post(self, token):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('UPDATE login_requests SET approved = ?, status = ? WHERE token = ?', (1, 'Approved', token))
        conn1.commit()
        
        conn1.close()

        return {'message': 'Login request approved'}

## REJECT MANAGER LOGIN REQUEST MODEL 
class RejectLoginRequest(Resource):
    def post(self, token):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('UPDATE login_requests SET approved = ?, status = ? WHERE token = ?', (0, 'Rejected', token))
        conn1.commit()
        
        conn1.close()

        return {'message': 'Login request rejected'}
    
## VERIFY USER CREDENTIALS METHOD  
def verify_user_credentials(username, password, role):
    conn1 = sqlite3.connect('storedata.db')
    conn1.row_factory = sqlite3.Row
    cursor1 = conn1.cursor()

    # Check if credentials are valid
    cursor1.execute('SELECT * FROM users WHERE username = ? AND password = ? AND role = ?', (username, password, role))
    user = cursor1.fetchone()

    if user is not None:
        user_id = user['id']
        role = user['role']
        conn1.close()
        return user_id, role
    
    conn1.close()
    return None
    

## LOGOUT MODEL 
class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt_identity()
            print(jti)
            return {'message': 'Successfully logged out'}, 200
        except Exception as e:
            return { 'message': 'Logout failed. Reason: {}'.format(str(e))}