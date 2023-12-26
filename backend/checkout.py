from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlite3
from cart import calculate_total_price

## ADMIN CHECKOUT MODEL
class AdminCheckout(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (user_id, 'admin'))
        cart = cursor1.fetchall()

        _, total_price = calculate_total_price(cart=cart)

        return {'total_price': total_price, 'admin_id': user_id}

## USER CHECKOUT MODEL
class UserCheckout(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (user_id, 'user'))
        cart = cursor1.fetchall()

        _, total_price = calculate_total_price(cart=cart)

        return {'total_price': total_price, 'user_id': user_id}
    
## MANAGER CHECKOUT MODEL
class ManagerCheckout(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (user_id, 'manager'))
        cart = cursor1.fetchall()

        _, total_price = calculate_total_price(cart=cart)

        return {'total_price': total_price, 'manager_id': user_id}
    

## ADMIN ORDERS METHOD
class AdminOrder(Resource):
    def post(self):
        data = request.get_json()
        admin_id = data.get('admin_id')
        role = data.get('role')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        try:
            cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (admin_id, role))
            cart = cursor1.fetchall()

            _, total_price = calculate_total_price(cart)

            for item in cart:
                admin_id = item[1]
                role = item[2]
                product_id = item[3]
                product_name = item[4]
                price = item[5]
                unit = item[6]
                image_path = item[7]
                quantity = int(item[8])

                cursor1.execute('INSERT INTO orders (user_id, role, product_id, name, price, unit, image_path, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (admin_id, role, product_id, product_name, price, unit, image_path, quantity, total_price))
                conn1.commit()

                cursor1.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))
                conn1.commit()

            cursor1.execute('DELETE FROM cart WHERE user_id = ? AND role = ?', (admin_id, 'admin'))
            conn1.commit()

            return {'message': 'Order completed successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        finally:
            conn1.close()
            conn1.close()
            conn1.close()
 
    @jwt_required()
    def get(self):
        admin_id = get_jwt_identity()

        if admin_id:
            conn1 = sqlite3.connect('storedata.db')
            cursor1 = conn1.cursor()

            cursor1.execute('SELECT * FROM orders WHERE user_id = ? AND role = ? ORDER BY created_at DESC', (admin_id, 'admin'))
            orders = cursor1.fetchall()

            total_price = calculate_total_expenditure(admin_id, 'admin')

            return { 'orders': orders, 'total_price': total_price}
        else:
            return {'message' : 'Please login'}
        
## USER ORDERS METHOD
class UserOrder(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        try:
            cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (user_id, 'user'))
            cart = cursor1.fetchall()

            _, total_price = calculate_total_price(cart)

            for item in cart:
                user_id = item[1]
                role = item[2]
                product_id = item[3]
                product_name = item[4]
                price = item[5]
                unit = item[6]
                image_path = item[7]
                quantity = int(item[8])

                cursor1.execute('INSERT INTO orders (user_id, role, product_id, name, price, unit, image_path, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, role, product_id, product_name, price, unit, image_path, quantity, total_price))
                conn1.commit()

                cursor1.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))
                conn1.commit()

            cursor1.execute('DELETE FROM cart WHERE user_id = ? AND role = ?', (user_id, 'user'))
            conn1.commit()

            return {'message': 'Order completed successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        finally:
            conn1.close()
          
 
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        if user_id:
            conn1 = sqlite3.connect('storedata.db')
            cursor1 = conn1.cursor()

            cursor1.execute('SELECT * FROM orders WHERE user_id = ? AND role = ? ORDER BY created_at DESC', (user_id, 'user'))
            orders = cursor1.fetchall()

            total_price = calculate_total_expenditure(user_id, 'user')


            return { 'orders': orders, 'total_price': total_price}
        else:
            return {'message' : 'Please login'}

## MANAGER ORDERS METHOD
class ManagerOrder(Resource):
    def post(self):
        data = request.get_json()
        manager_id = data.get('manager_id')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        try:
            cursor1.execute('SELECT * FROM cart WHERE user_id = ? AND role = ?', (manager_id, 'manager'))
            cart = cursor1.fetchall()

            _, total_price = calculate_total_price(cart)

            for item in cart:
                manager_id = item[1]
                role = item[2]
                product_id = item[3]
                product_name = item[4]
                price = item[5]
                unit = item[6]
                image_path = item[7]
                quantity = int(item[8])

                cursor1.execute('INSERT INTO orders (user_id, role, product_id, name, price, unit, image_path, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (manager_id, role, product_id, product_name, price, unit, image_path, quantity, total_price))
                conn1.commit()

                cursor1.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (quantity, product_id))
                conn1.commit()

            cursor1.execute('DELETE FROM cart WHERE user_id = ? AND role = ?', (manager_id, 'manager'))
            conn1.commit()

            return {'message': 'Order completed successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        finally:
            conn1.close()
            conn1.close()
            conn1.close()
 
    @jwt_required()
    def get(self):
        manager_id = get_jwt_identity()

        if manager_id:
            conn1 = sqlite3.connect('storedata.db')
            cursor1 = conn1.cursor()

            cursor1.execute('SELECT * FROM orders WHERE user_id = ? AND role = ? ORDER BY created_at DESC', (manager_id, 'manager'))
            orders = cursor1.fetchall()

            total_price = calculate_total_expenditure(manager_id, 'manager')


            return { 'orders': orders, 'total_price': total_price}
        else:
            return {'message' : 'Please login'}

## Calculate total extenditure function 
def calculate_total_expenditure(user_id, role):
    conn1 = sqlite3.connect('storedata.db')
    cursor1 = conn1.cursor()

    cursor1.execute('SELECT * FROM orders WHERE user_id = ? AND role = ? ORDER BY created_at DESC', (user_id, role))
    orders = cursor1.fetchall()
    total = 0
    
    for order in orders:
        total += order[9]
    return total