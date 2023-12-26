from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlite3

## PRODUCT MODEL/METHOD    
class Product(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        product_name = data.get('product_name')
        price = data.get('price')
        product_unit = data.get('product_unit')
        expiry_date = data.get('expiry_date')
        image_path = data.get('image_path')
        quantity = data.get('quantity')
        category_id = data.get('category_id')
        role = data.get('role')
        user_id = get_jwt_identity()

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM products WHERE product_name = ? AND price = ? AND product_unit = ? AND expiry_date = ? AND image_path = ? AND quantity = ? AND category_id = ?', (product_name, price, product_unit, expiry_date, image_path, quantity, category_id))

        if cursor1.fetchone() is not None:
            return {'message': 'Product already exists'}, 400
        
        # Insert a new user into the database
        cursor1.execute('INSERT INTO products (product_name, price, product_unit, expiry_date, image_path, quantity, category_id, user_id, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (product_name, price, product_unit, expiry_date, image_path, quantity, category_id, user_id, role))
        conn1.commit()
        conn1.close()

        return {'message': 'Product added successfully'}, 201

## PRODUCT LIST MODEL/METHOD    
class ProductList(Resource):
    def get(self):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()
        #Check if username already exists
        cursor1.execute('SELECT * FROM products ORDER BY created_at DESC')
        products = cursor1.fetchall()

        # Create a dictionary to storedata products grouped by category
        products_by_category = {}
        for product in products:
            category_id = product[7]

            if category_id not in products_by_category:
                products_by_category[category_id] = []
            product_dict = {
                'id': product[0],
                'product_name': product[1],
                'price': product[2],
                'product_unit': product[3],
                'expiry_date': product[4],
                'image_path': product[5],
                'quantity': product[6]
            }
            products_by_category[category_id].append(product_dict)
        
        cursor1.execute('SELECT * FROM category')
        categories = cursor1.fetchall()

        category_dict = {}
        for category in categories:
            category_dict[category[0]] = category[1]
        
        conn1.close()

        product_list = []

        for id, name in category_dict.items():
            products = products_by_category.get(id, [])
            product_list.append({'category_id': id, 'category_name': name, 'products': products})

        return {'products': product_list}
    
## EDIT PRODUCT MODEL/METHOD    
class EditProduct(Resource):  
    def get(self, product_id):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor1.fetchone()

        cursor1.execute('SELECT * FROM category')
        categories = cursor1.fetchall()

        if product is not None:
            return {'product': product, 'categories': categories}
        return {'message': 'Product not found'}, 404
    
    def put(self, product_id):
        data = request.get_json()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        name = data.get('product_name')
        price = data.get('price')
        unit = data.get('product_unit')
        expiry_date = data.get('expiry_date')
        image_path = data.get('image_path')
        quantity = data.get('quantity')
        category_id = data.get('category_id')

        cursor1.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor1.fetchone()

        if product is not None:
            cursor1.execute('UPDATE products SET product_name = ?, price = ?, product_unit = ?, expiry_date = ?, image_path = ?, quantity = ?, category_id = ? WHERE id = ?', (name, price, unit, expiry_date, image_path, quantity, category_id, product_id))
            conn1.commit()
            return {'message': 'Product updated successfully'}
        return {'message': 'Product not found'}, 404
    
## DELETE PRODUCT MODEL/METHOD    
class DeleteProduct(Resource):
    def delete(self, product_id):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('DELETE FROM products WHERE id = ?', (product_id,))

        conn1.commit()
        conn1.close()

        return {'message': 'Category and associated products deleted successfully'}
    
## SEARCH PRODUCT MODEL/METHOD    
class ProductSearch(Resource):
    def get(self, query):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        product_list = []
        result = []

        ## Result when user search product by product name
        cursor1.execute('SELECT * FROM products WHERE product_name LIKE ?', ('%' + query + '%',))
        products = cursor1.fetchall()

        for product in products:
            cursor1.execute('SELECT name FROM category WHERE id LIKE ?', (product[7],))
            category_name = cursor1.fetchone()
            product_list.append({'category_id': product[7], 'category_name': category_name[0], 'products': products})

        result.extend(product_list)

        ## Result when user search product by category name
        cursor1.execute('SELECT * FROM category WHERE name LIKE ?', ('%' + query + '%',))
        categories = cursor1.fetchall()

        for category in  categories:
            cursor1.execute('SELECT * FROM products WHERE category_id = ?', (category[0],))
            product_by_category = cursor1.fetchall()
            cursor1.execute('SELECT name FROM category WHERE id LIKE ?', (category[0],))
            category_name = cursor1.fetchone()
            product_list.append({'category_id': category[0], 'category_name': category_name[0], 'products': product_by_category})

            result.extend(product_list)
        
        conn1.close()

        return {'query': result}
    
    