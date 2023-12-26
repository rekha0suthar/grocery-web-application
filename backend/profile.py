from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlite3
from cache_config import cache

## ADMIN PROFILE MODEL
class AdminProfile(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            admin_profile = get_profile(current_user_id, 'admin')

            if admin_profile:
                return {'profile_data': admin_profile}, 200  # Assuming admin_profile is a dictionary
            else:
                return {'message': 'Admin profile not found'}, 404
        except Exception as e:
            return {'message': 'Error fetching admin profile', 'error': str(e)}, 500

    
## USER PROFILE MODEL
class UserProfile(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            user_profile = get_profile(current_user_id, 'user')

            if user_profile:
                return {'profile_data': user_profile}, 200  # Assuming user_profile is a dictionary
            else:
                return {'message': 'User profile not found'}, 404
        except Exception as e:
            return {'message': 'Error fetching user profile', 'error': str(e)}, 500


## MANAGER PROFILE MODEL
class ManagerProfile(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            manager_profile = get_profile(current_user_id, 'manager')

            if manager_profile:
                return {'profile_data': manager_profile}, 200  # Assuming user_profile is a dictionary
            else:
                return {'message': 'Manager profile not found'}, 404
        except Exception as e:
            return {'message': 'Error fetching manager profile', 'error': str(e)}, 500

def get_profile(user_id, role):
    conn1 = sqlite3.connect('storedata.db')
    cursor1 = conn1.cursor()

    cursor1.execute('SELECT * FROM users WHERE id = ? AND role = ?', (user_id, role))
    existing_user = cursor1.fetchone()

    if existing_user is not None:
        return existing_user
    else:
        return {'message': 'User not found'}