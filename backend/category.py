from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlite3

## CATEGORY MODEL/METHOD   
class Category(Resource):
    def post(self):
        data = request.get_json()
        category_name = data.get('name')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()
        #Check if category already exists
        cursor1.execute('SELECT * FROM category WHERE name = ?', (category_name,))
        if cursor1.fetchone() is not None:
            return {'message': 'Category already exists'}, 400
        
        # Insert a new user into the database
        cursor1.execute('INSERT INTO category (name) VALUES (?)', (category_name,))
        conn1.commit()

        return {'message': 'Category added successfully'}, 201

## CATEGORY LIST MODEL/METHOD
class CategoryList(Resource):
    def get(self):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM category')
        categories = cursor1.fetchall()

        return {'categories': categories}
    
## EDIT CATEGORY MODEL/METHOD    
class EditCategory(Resource):  
    conn1 = sqlite3.connect('storedata.db')
    cursor1 = conn1.cursor()

    #Check if category already exists
    def get(self, category_id):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM category WHERE id = ?', (category_id,))
        category = cursor1.fetchone()

        if category is not None:
            return {'category': category[1]}
        return {'message': 'Category not found'}, 404
    
    def put(self, category_id):
        data = request.get_json()
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        new_name = data.get('category_name')
        cursor1.execute('SELECT * FROM category WHERE id = ?', (category_id,))
        category = cursor1.fetchone()

        if category is not None:
            cursor1.execute('UPDATE category SET name = ? WHERE id = ?', (new_name, category_id))
            conn1.commit()
            return {'message': 'Category updated successfully'}
        return {'message': 'Category not found'}, 404
    
## DELETE CATEGORY MODEL/METHOD    
class DeleteCategory(Resource):
    def delete(self, category_id):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('DELETE FROM category WHERE id = ?', (category_id,))
        cursor1.execute('DELETE FROM products WHERE category_id = ?', (category_id,))

        conn1.commit()
        conn1.close()

        return {'message': 'Category and associated products deleted successfully'}

## REQUEST ADD CATEGORY MODEL/METHOD
class RequestAddCategory(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        category_name = data.get('name')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()
        cursor1.execute('SELECT first_name, last_name FROM users WHERE id = ? AND role = ?', (current_user_id, 'manager'))
        name = cursor1.fetchone()

        full_name = name[0] + " " + name[1]

        #Check if category already exists
        cursor1.execute('SELECT * FROM category WHERE name = ?', (category_name,))
        category = cursor1.fetchone()

        cursor1.execute('SELECT * FROM category_requests WHERE name = ? AND request_type = ?', (category_name, 'Add'))
        cat_req = cursor1.fetchone()
       
        if category is not None:
            return {'message': 'Category already exists', 'name':name}, 400
        else:
            if cat_req is not None:
                return {'message': 'Category request already sent, wait for approval'}, 400
            
            # Insert a new request into the database
            cursor1.execute('INSERT INTO category_requests (name, status, manager_name, request_type) VALUES (?, ?, ?, ?)', (category_name, 'Pending', full_name, 'Add'))
            conn1.commit()
            conn1.close()

            return {'message': 'Category request send successfully'}, 201
    def get(self):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM category_requests')
        cat_reqs = cursor1.fetchall()

        conn1.close()

        return {'cat_requests': cat_reqs}

## APPROVE REQUEST ADD CATEGORY MODEL/METHOD
class ApproveAddCategoryRequest(Resource):
    def post(self):
        data = request.get_json()
        request_id = data.get('request_id')
        category_name = data.get('category_name')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('UPDATE category_requests SET status = ? WHERE id = ? AND request_type = ?', ("Approved", request_id, 'Add'))
        conn1.commit()

        cursor1.execute('INSERT INTO category (name) VALUES (?)', (category_name,))
        conn1.commit()
        conn1.close()

        return {'message': 'Requested category has been approved and added'}, 200

## REJECT REQUEST ADD CATEGORY MODEL/METHOD
class RejectAddCategoryRequest(Resource):
    def post(self):
        data = request.get_json()
        request_id = data.get('request_id')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('UPDATE category_requests SET status = ? WHERE id = ? AND request_type = ?', ("Rejected", request_id, 'Add'))
        conn1.commit()
        conn1.close()

        return {'message': 'Request to add category has been rejected'}, 200

## REQUEST DELETE CATEGORY MODEL/METHOD
class RequestDeleteCategory(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        category_id = data.get('category_id')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT first_name, last_name FROM users WHERE id = ? AND role = ?', (current_user_id, 'manager'))
        name = cursor1.fetchone()

        full_name = name[0] + " " + name[1]
        
        #Check if category already exists
        cursor1.execute('SELECT name FROM category WHERE id = ?', (category_id,))
        category_name = cursor1.fetchone()

        cursor1.execute('SELECT * FROM category_requests WHERE name = ? AND request_type = ?', (category_name[0], 'Delete'))
        cat_req = cursor1.fetchone()
        if cat_req is not None:
            return {'message': 'Request to delete this category is already sent, wait for approval'}, 400
        else:
            # Insert a new request into the database
            cursor1.execute('INSERT INTO category_requests (name, status, manager_name, request_type) VALUES (?, ?, ?, ?)', (category_name[0], 'Pending', full_name, 'Delete'))
            conn1.commit()
            conn1.close()

            return {'message': 'Category delete request send successfully'}, 201

## APPROVE REQUEST DELETE CATEGORY MODEL/METHOD
class ApproveDeleteCategoryRequest(Resource):
    ## Delete Category Model and api    
    def delete(self, category_name, request_id):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()
        
        cursor1.execute('SELECT * FROM category WHERE name = ?', (category_name,))
        category_id = cursor1.fetchone()
        
        cursor1.execute('DELETE FROM category WHERE name = ?', (category_name,))
        
        cursor1.execute('DELETE FROM products WHERE category_id = ?', (category_id[0],))

        cursor1.execute('UPDATE category_requests SET status = ? WHERE id = ? AND request_type = ?', ("Approved", request_id, 'Delete'))
        conn1.commit()
        conn1.close()

        return {'message': 'Category and associated products deleted successfully'}

## REJECT REQUEST DELETE CATEGORY MODEL/METHOD
class RejectDeleteCategoryRequest(Resource):
    ## Delete Category Model and api    
    def post(self, request_id):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('UPDATE category_requests SET status = ? WHERE id = ? AND request_type = ?', ("Rejected", request_id, 'Delete'))

        conn1.commit()
        conn1.close()

        return {'message': 'Request to delete category has been rejected'}
    
## REQUEST EDIT CATEGORY MODEL/METHOD
class RequestEditCategory(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        category_id = int(data.get('category_id'))
        new_name = data.get('category_name')
        
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT first_name, last_name FROM users WHERE id = ? AND role = ?', (current_user_id, 'manager'))
        name = cursor1.fetchone()

        full_name = name[0] + " " + name[1]

         #Check if category already exists
        cursor1.execute('SELECT name FROM category WHERE id = ?', (category_id,))
        category_name = cursor1.fetchone()

        cursor1.execute('SELECT * FROM category_requests WHERE name = ? AND request_type = ? AND category_id = ?', (new_name, 'Edit', category_id))
        cat_req = cursor1.fetchone()
        print(cat_req)
        if cat_req is not None:
            return {'message': 'Your request is already sent', 'data': cat_req}, 201
        else:
            # Insert a new request into the database
            cursor1.execute('INSERT INTO category_requests (name, status, manager_name, request_type, category_id) VALUES (?, ?, ?, ?, ?)', (new_name, 'Pending', full_name, 'Edit', category_id))
            conn1.commit()
            conn1.close()

            return {'message': 'Category edit request send successfully', 'data': cat_req}, 201

## APPROVE REQUEST EDIT CATEGORY MODEL/METHOD
class ApproveEditCategoryRequest(Resource):
    def put(self):
        data = request.get_json()
        request_id = data.get('request_id')
        new_name = data.get('category_name')

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM category_requests WHERE name = ? AND request_type = ? AND id = ?', (new_name, 'Edit', request_id))
        cat_req = cursor1.fetchone()

        cursor1.execute('SELECT * FROM category WHERE id = ?', (cat_req[5],))
        category = cursor1.fetchone()

        if category is not None:
            cursor1.execute('UPDATE category_requests SET status = ? WHERE id = ? AND request_type = ?', ("Approved", request_id, 'Edit'))
            cursor1.execute('UPDATE category SET name = ? WHERE id = ?', (new_name, cat_req[5]))
            conn1.commit()
            conn1.close()
            return {'message': 'Category updated successfully'}, 200
        else:
            return {'message': 'Category not found'}, 404

## REJECT REQUEST EDIT CATEGORY MODEL/METHOD
class RejectEditCategoryRequest(Resource):
    def post(self, request_id):
        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('UPDATE category_requests SET status = ? WHERE id = ? AND request_type = ?', ("Rejected", request_id, 'Edit'))

        conn1.commit()
        conn1.close()

        return {'message': 'Request to edit category has been rejected'}