from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Car:
    def __init__(self,data):
        self.id = data['id']
        self.seller_id = data['seller_id']
        self.price = data['price']
        self.model= data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updatd_at = data['updated_at']
    

    @classmethod
    def add_car(cls,data):
        query="""
              INSERT INTO cars(seller_id,price,model,make,year,description)
              VALUES(%(seller_id)s,%(price)s,%(model)s,%(make)s,%(year)s,%(description)s);
              """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all_cars(cls):
        query ="SELECT* FROM cars LEFT JOIN sellers ON cars.seller_id = sellers.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_cars = []
        if results:
            for row in results:
                car = cls(row)
                car.seller = f"{row['first_name']} {row['last_name']}"
                all_cars.append(car)
        return all_cars
  


    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT* FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update_car(cls, data):
        query = """
            UPDATE cars SET 
                price = %(price)s, 
                model= %(model)s,
                make = %(make)s, 
                year = %(year)s, 
                description = %(description)s,
                updated_at = NOW() 
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
            
    

    @staticmethod
    def validate(data):
        is_valid = True
        if data['model'] == "":
            is_valid = False
            flash("the model field is required","register_car")
        if data['make'] == "":
            is_valid = False
            flash("the make field is required","register_car")
        if  data['price'] == "":
           is_valid = False
           flash("the price flied is required","register_car")
        elif float(data['price']) <= 0:
           is_valid = False
           flash("the price must be greater than 0","register_car")
        if  data['year'] == "":
            is_valid = False
            flash("the yearflied is required","register_car")
        elif float(data['year']) <= 0:
           is_valid = False
           flash("the year must be greater than 0","register_car")
        if data['description'] =="":
            is_valid = False
            flash("Description greater than 6","register_car")
        return is_valid

    

    
   