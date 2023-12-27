from flask import Flask, request, jsonify,send_file
import sqlite3
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from cache_config import cache
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from category import Category, CategoryList, EditCategory, DeleteCategory, RequestAddCategory, RequestDeleteCategory, RequestEditCategory, ApproveEditCategoryRequest, ApproveDeleteCategoryRequest, RejectAddCategoryRequest, RejectDeleteCategoryRequest, RejectEditCategoryRequest, ApproveAddCategoryRequest
from product import Product, ProductList, EditProduct, DeleteProduct, ProductSearch
from cart import AdminCart, UserCart, ManagerCart, RemoveFromCart, updateQuantity
from checkout import AdminCheckout, ManagerCheckout, UserCheckout, AdminOrder, ManagerOrder, UserOrder, calculate_total_expenditure
from users import Register, UserLogin, AdminLogin, ManagerLoginRequest, ApproveLoginRequest, RejectLoginRequest, verify_user_credentials, LoginRequests, Logout
from profile import UserProfile, ManagerProfile, AdminProfile
from task import generate_monthly_report, export_product_detail_as_csv

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)

cache.init_app(app)

app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set your desired token expiration time
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Set your desired refresh token expiration time


## creating users database with sqlite
conn1 = sqlite3.connect('storedata.db')
cursor1 = conn1.cursor()

## crearting users table to store User/Admin/Store-manager/LoginRequests credentials
cursor1.execute('''
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      role TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL
    )
''')

cursor1.execute('''
    CREATE TABLE IF NOT EXISTS login_requests (
      id INTEGER PRIMARY KEY,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      token TEXT,
      approved BOOLEAN,
      status TEXT NOT NULL
    )
''')

cursor1.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        product_unit TEXT NOT NULL,
        expiry_date DATE,
        image_path TEXT,
        quantity INTEGER NOT NULL,
        category_id INTEGER,
        user_id INTEGER,
        role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES category (id) ON DELETE CASCADE
    )
''')

cursor1.execute('''
    CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
''')

cursor1.execute('''
    CREATE TABLE IF NOT EXISTS category_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        status TEXT NOT NULL,
        manager_name TEXT NOT NULL,
        request_type TEXT NOT NULL,
        category_id INTEGER
    )
''')


cursor1.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT NOT NULL,
        product_id INTEGER,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        unit TEXT NOT NULL,
        image_path TEXT,
        quantity INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')

cursor1.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT NOT NULL,
        product_id INTEGER,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        unit TEXT NOT NULL,
        image_path TEXT,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')

conn1.commit()
conn1.close()    


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

## PROFILE APIS

api.add_resource(AdminProfile, '/admin/profile')
api.add_resource(UserProfile, '/user/profile')
api.add_resource(ManagerProfile, '/store_manager/profile')

## CATEGORY APIS
        
api.add_resource(Category, '/admin/add_category')    
api.add_resource(CategoryList, '/get_categories')
api.add_resource(EditCategory, '/admin/edit_category/<int:category_id>')
api.add_resource(DeleteCategory, '/admin/delete_category/<int:category_id>')

# MANAGER REQUEST TO ADD, EDIT AND DELETE CATEGORY
##Category Model and api    
api.add_resource(RequestAddCategory, '/store_manager/request_add_category')
api.add_resource(ApproveAddCategoryRequest, '/approve/add_category_request')
api.add_resource(RejectAddCategoryRequest, '/reject/add_category_request')
api.add_resource(RequestDeleteCategory, '/store_manager/request_delete_category')
api.add_resource(ApproveDeleteCategoryRequest, '/approve/delete_category_request/<string:category_name>/<int:request_id>')
api.add_resource(RejectDeleteCategoryRequest, '/reject/delete_category_request/<int:request_id>')
api.add_resource(RequestEditCategory, '/store_manager/request_edit_category')
api.add_resource(ApproveEditCategoryRequest, '/approve/edit_category_request')
api.add_resource(RejectEditCategoryRequest, '/reject/edit_category_request/<int:request_id>')

## PRODUCT api            
api.add_resource(Product, '/add_product')
api.add_resource(ProductList, '/get_products')
api.add_resource(EditProduct, '/edit_product/<int:product_id>')
api.add_resource(DeleteProduct, '/delete_product/<int:product_id>')
api.add_resource(ProductSearch, '/search/<string:query>')

## CART API
api.add_resource(AdminCart, '/admin/cart')
api.add_resource(UserCart, '/user/cart')
api.add_resource(ManagerCart, '/store_manager/cart')
api.add_resource(RemoveFromCart, '/remove_from_cart/<int:product_id>/<string:role>')
api.add_resource(updateQuantity, '/update_quantity/<int:product_id>')

##CHECKOUT API 
    
api.add_resource(AdminCheckout, '/admin/checkout')
api.add_resource(ManagerCheckout, '/store_manager/checkout')
api.add_resource(UserCheckout, '/user/checkout')

##ORDERS API

api.add_resource(AdminOrder, '/admin/orders')
api.add_resource(UserOrder, '/user/orders')
api.add_resource(ManagerOrder, '/store_manager/orders')



@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({'message': f'Protected route, user ID: {current_user_id}'})

@app.route('/store_manager/export_csv_report', methods=['POST'])
@jwt_required()
def trigger_export_csv():
    manager_id = get_jwt_identity()
    task = export_product_detail_as_csv.apply_async(args=[manager_id])
    result = task.get()
    return send_file(result, as_attachment=True)


generate_monthly_report.apply_async()


if __name__ == "__main__":
    app.run(debug=True)
