from flask import render_template, redirect, request,session
from flask_app import app
from flask_app.models.seller import Seller
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt    
bcrypt = Bcrypt(app) 
from flask import flash 


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    if not Seller.validate(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Seller.register(data)
    session['seller_id'] = id

    return redirect('/dashboard')



@app.route('/login', methods = ['post'])
def login():
    seller_form_db = Seller.get_by_email({'email':request.form['email']})
    if seller_form_db:
        if not bcrypt.check_password_hash(seller_form_db.password, request.form['password']):
            flash("Invalid Email/Password","login")
            return redirect('/')
        else :
            session['seller_id'] = seller_form_db.id
            return redirect ('/dashboard')
    flash("Invalid Email/Password","login")
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
