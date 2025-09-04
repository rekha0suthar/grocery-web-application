from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from cache_config import cache
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from database import get_db_connection, init_database
from users_postgres import Register, UserLogin, AdminLogin, ManagerLoginRequest, ApproveLoginRequest, RejectLoginRequest, LoginRequests, Logout

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)

cache.init_app(app)

app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize database tables
init_database()

## API ROUTES
## REGISTER API
api.add_resource(Register, '/get_token')

## LOGIN API
api.add_resource(UserLogin, '/user/login')
api.add_resource(ManagerLoginRequest, '/store_manager/login')
api.add_resource(AdminLogin, '/admin/login')

## MANAGER LOGIN REQUEST API
api.add_resource(LoginRequests, '/admin/login_requests')
api.add_resource(ApproveLoginRequest, '/approve_login_requests/<string:token>')
api.add_resource(RejectLoginRequest, '/reject_login_requests/<string:token>')

## LOGOUT API
api.add_resource(Logout, '/logout')

## HEALTH CHECK
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Grocery Store API is running'})

## ROOT ENDPOINT
@app.route('/')
def root():
    return jsonify({'message': 'Grocery Store API', 'version': '1.0.0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
