from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import re	  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Seller:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updatd_at = data['updated_at']
    
    @classmethod
    def register(cls,data):
        query="INSERT INTO sellers(first_name,last_name,email,password)VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query="SELECT* FROM sellers;"
        results = connectToMySQL(DATABASE).query_db(query)
        sellers = []
        for row in results:
           sellers.append( cls(row))
        return sellers
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM sellers WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM sellers WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name'])<3:
            is_valid = False
            flash("First name must be at least 3 characters","register")
        if len(data['last_name'])<3:
            is_valid = False
            flash("Last name must be at least 3 characters","register")
        if not EMAIL_REGEX.match(data['email']):               
            is_valid = False
            flash("Email not valid")
        elif Seller.get_by_email({'email':data['email']}):
            is_valid = False
            flash("Email Already Exist","register")
        if len(data['password'])<8:
            is_valid = False
            flash("Password must be at least 8","register")
        elif data['password']!= data['confirm_password']:
            is_valid = False
            flash("Password and Confirm password must match","register")
        return is_valid