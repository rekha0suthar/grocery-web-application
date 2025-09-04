from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt_identity
from database import get_db_connection, get_cursor
import os

def verify_user_credentials(username, password, role):
    """Verify user credentials and return user info"""
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, username, role FROM users WHERE username = %s AND password = %s AND role = %s', 
                      (username, password, role))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Error verifying credentials: {e}")
        return None
    finally:
        conn.close()

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

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            # Check if user already exists
            cursor.execute('SELECT * FROM users WHERE username = %s AND role = %s', (username, role))
            existing_user = cursor.fetchone()

            if existing_user:
                return jsonify({'message': 'Username already exists'}), 400

            # Insert the user data into the database
            cursor.execute('INSERT INTO users (first_name, last_name, username, password, role, email) VALUES (%s, %s, %s, %s, %s, %s)', 
                          (first_name, last_name, username, password, role, email))
            conn.commit()

            # Get user info and create tokens
            user_info = verify_user_credentials(username, password, role)

            if user_info:
                access_token = create_access_token(identity=user_info[0])
                refresh_token = create_refresh_token(identity=user_info[0])
                return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
            else:
                return jsonify({'message': 'Invalid credentials'})
                
        except Exception as e:
            print(f"Error in registration: {e}")
            conn.rollback()
            return jsonify({'message': 'Registration failed'}), 500
        finally:
            conn.close()

## ADMIN LOGIN MODEL 
class AdminLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user_info = verify_user_credentials(username, password, 'admin')
        
        if user_info:
            access_token = create_access_token(identity=user_info[0])
            refresh_token = create_refresh_token(identity=user_info[0])
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

## USER LOGIN MODEL
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user_info = verify_user_credentials(username, password, 'user')
        
        if user_info:
            access_token = create_access_token(identity=user_info[0])
            refresh_token = create_refresh_token(identity=user_info[0])
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

## MANAGER LOGIN REQUEST MODEL
class ManagerLoginRequest(Resource):
    def post(self):
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            # Check if username already exists in login_requests
            cursor.execute('SELECT * FROM login_requests WHERE username = %s', (username,))
            existing_request = cursor.fetchone()

            if existing_request:
                return jsonify({'message': 'Login request already exists'}), 400

            # Insert login request
            cursor.execute('INSERT INTO login_requests (first_name, last_name, username, password, role, email, status) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                          (first_name, last_name, username, password, 'store_manager', email, 'pending'))
            conn.commit()
            
            return jsonify({'message': 'Login request submitted successfully'})
            
        except Exception as e:
            print(f"Error in manager login request: {e}")
            conn.rollback()
            return jsonify({'message': 'Request submission failed'}), 500
        finally:
            conn.close()

## LOGIN REQUESTS LIST MODEL
class LoginRequests(Resource):
    @jwt_required()
    def get(self):
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM login_requests WHERE status = %s', ('pending',))
            requests = cursor.fetchall()
            
            # Convert to list of dictionaries
            requests_list = []
            for req in requests:
                requests_list.append({
                    'id': req[0],
                    'first_name': req[1],
                    'last_name': req[2],
                    'username': req[3],
                    'email': req[6],
                    'status': req[7]
                })
            
            return jsonify(requests_list)
            
        except Exception as e:
            print(f"Error fetching login requests: {e}")
            return jsonify({'message': 'Failed to fetch requests'}), 500
        finally:
            conn.close()

## APPROVE LOGIN REQUEST MODEL
class ApproveLoginRequest(Resource):
    @jwt_required()
    def post(self, token):
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            # Get the login request
            cursor.execute('SELECT * FROM login_requests WHERE id = %s', (token,))
            request_data = cursor.fetchone()
            
            if not request_data:
                return jsonify({'message': 'Request not found'}), 404
            
            # Insert into users table
            cursor.execute('INSERT INTO users (first_name, last_name, username, password, role, email) VALUES (%s, %s, %s, %s, %s, %s)', 
                          (request_data[1], request_data[2], request_data[3], request_data[4], request_data[5], request_data[6]))
            
            # Update request status
            cursor.execute('UPDATE login_requests SET status = %s WHERE id = %s', ('approved', token))
            
            conn.commit()
            return jsonify({'message': 'Login request approved successfully'})
            
        except Exception as e:
            print(f"Error approving login request: {e}")
            conn.rollback()
            return jsonify({'message': 'Failed to approve request'}), 500
        finally:
            conn.close()

## REJECT LOGIN REQUEST MODEL
class RejectLoginRequest(Resource):
    @jwt_required()
    def post(self, token):
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            # Update request status
            cursor.execute('UPDATE login_requests SET status = %s WHERE id = %s', ('rejected', token))
            conn.commit()
            
            return jsonify({'message': 'Login request rejected successfully'})
            
        except Exception as e:
            print(f"Error rejecting login request: {e}")
            conn.rollback()
            return jsonify({'message': 'Failed to reject request'}), 500
        finally:
            conn.close()

## LOGOUT MODEL
class Logout(Resource):
    @jwt_required()
    def post(self):
        return jsonify({'message': 'Successfully logged out'})
