from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlite3

## ADMIN CART METHOD
class AdminCart(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        product_id = data.get('product_id')
        product_name = data.get('product_name')
        price = data.get('price')
        product_unit = data.get('product_unit')
        image_path = data.get('image_path')
        role = data.get('role')

        quantity = 1
        user_id = get_jwt_identity()

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ? AND product_id = ?', (user_id, role, product_id))
        item = cursor1.fetchone()

        if item:
            return {'message': 'Product already exist in cart'}, 400
        else:
            cursor1.execute('INSERT INTO cart (user_id, role, product_id, name, price, unit, image_path, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, role, product_id, product_name, price, product_unit, image_path, quantity ))
            conn1.commit()

            return {'message': 'Product added to cart succesfully'}, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (user_id, 'admin'))
        items = cursor1.fetchall()

        total_count, total_price = calculate_total_price(items)

        if items is not None:
            return {'products': items, 'total_count': total_count, 'total_price': total_price, 'user_id': user_id }
        else:
            return {'message': 'No product found in cart'}
        
        
## USER CART METHOD
class UserCart(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        product_id = data.get('product_id')
        product_name = data.get('product_name')
        price = data.get('price')
        product_unit = data.get('product_unit')
        image_path = data.get('image_path')
        role = data.get('role')

        quantity = 1
        user_id = get_jwt_identity()

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ? AND product_id = ?', (user_id, role, product_id))
        item = cursor1.fetchone()

        if item:
            return {'message': 'Product already exist in cart'}, 400
        else:
            cursor1.execute('INSERT INTO cart (user_id, role, product_id, name, price, unit, image_path, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, role, product_id, product_name, price, product_unit, image_path, quantity ))
            conn1.commit()

            return {'message': 'Product added to cart succesfully'}, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (user_id, 'user'))
        items = cursor1.fetchall()

        total_count, total_price = calculate_total_price(items)

        if items is not None:
            return {'products': items, 'total_count': total_count, 'total_price': total_price, 'user_id': user_id }
        else:
            return {'message': 'No product found in cart'}
        
        
## STORE MANAGER CART MEHTOD
class ManagerCart(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        product_id = data.get('product_id')
        product_name = data.get('product_name')
        price = data.get('price')
        product_unit = data.get('product_unit')
        image_path = data.get('image_path')
        role = data.get('role')
        quantity = 1
        user_id = get_jwt_identity()

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ? AND product_id = ?', (user_id, role, product_id))
        item = cursor1.fetchone()

        if item:
            return {'message': 'Product already exist in cart'}, 400
        else:
            cursor1.execute('INSERT INTO cart (user_id, role, product_id, name, price, unit, image_path, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, role, product_id, product_name, price, product_unit, image_path, quantity ))
            conn1.commit()

            return {'message': 'Product added to cart succesfully'}, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (user_id, 'manager'))
        items = cursor1.fetchall()

        total_count, total_price = calculate_total_price(items)

        if items is not None:
            return {'products': items, 'total_count': total_count, 'total_price': total_price, 'user_id': user_id }
        else:
            return {'message': 'No product found in cart'}
        


## DELETE PRODUCT METHOD
class RemoveFromCart(Resource):
    @jwt_required()
    def delete(self, product_id, role):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()
        user_id = get_jwt_identity()


        cursor1.execute('DELETE FROM cart WHERE product_id = ? AND user_id = ? AND role = ?', (product_id, user_id, role))

        conn1.commit()
        conn1.close()

        return {'message': 'product removed from cart successfully'}
    
## UPDATE QUANTITY METHOD
class updateQuantity(Resource):
    @jwt_required()
    def put(self, product_id):
        data = request.get_json()
        quantity = data.get('quantity')
        role = data.get('role')
        user_id = get_jwt_identity()
  
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT quantity FROM products WHERE id = ?', (product_id,))
        product_quantity = cursor1.fetchone()

        cursor1.execute('SELECT quantity FROM cart WHERE product_id = ? AND role = ? AND user_id = ?', (product_id, role, user_id))
        update_quantity = cursor1.fetchone()        

        if quantity <= product_quantity[0]:
            cursor1.execute('UPDATE cart SET quantity = ? WHERE product_id = ? AND user_id = ? AND role = ?', (quantity, product_id, user_id, role))
            conn1.commit()
        else:
            quantity = product_quantity[0]
            cursor1.execute('UPDATE cart SET quantity = ? WHERE product_id = ? AND user_id = ? AND role = ?', (quantity, product_id, user_id, role))
            conn1.commit()

        cursor1.execute('SELECT * FROM cart WHERE product_id = ? AND role = ? AND user_id = ?', (product_id, role, user_id))
        cart = cursor1.fetchall()
        conn1.close()

        total_items, total_price = calculate_total_price(cart)
        
        return {'quantity': update_quantity[0], 'total_items': total_items, 'total_price': total_price }
    
## Calculate total price function
def calculate_total_price(cart):
    total_price = 0
    total_count = 0

    for product in cart:
        total_count += 1
        price = product[5]
        quantity = product[8]

        total_price += price * quantity
    return total_count, total_price