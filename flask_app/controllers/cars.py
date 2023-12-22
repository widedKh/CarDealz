from flask import render_template, redirect, request,session,flash
from flask_app import app
from flask_app.models.seller import Seller
from flask_app.models.car import Car

@app.route('/new')
def new_car():
    if 'seller_id' not in session:
        return redirect('/')
    return render_template("add_car.html")


@app.route('/cars/register', methods=['post'])
def add_car():
    if not Car.validate(request.form):
        return redirect('/new')
 
    data = {
        **request.form, 'seller_id':session['seller_id']
    }
    car_id = Car.add_car(data)
    if car_id:
        return redirect('/dashboard')
    else:
        flash("Failed to add car", "register_car")
        return redirect('/new')

    
@app.route('/dashboard')
def dashboard():
    if 'seller_id' not in session:
        return redirect('/')
    all_cars = Car.get_all_cars()
    logged_seller = Seller.get_by_id({'id':session['seller_id']})
    return render_template("dashboard.html", all_cars= all_cars, seller = logged_seller)


@app.route('/show/<int:id>')
def show_car(id):
    if 'seller_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    car= Car.get_by_id(data)
    seller_data = {
        "id": session['seller_id']
    }
    seller = Seller.get_by_id(seller_data)
    return render_template("show_car.html", car=car, seller=seller)

@app.route('/edit/<int:car_id>')
def edit_car(car_id):
    if 'seller_id' not in session:
        return redirect('/')
    
    car = Car.get_by_id({'id': car_id})
    
    return render_template('edit_car.html', car=car)


@app.route('/update', methods=['POST'])
def update_car():
    if 'seller_id' not in session:
        return redirect('/logout')
    if not Car.validate(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    data = {
        "price": request.form["price"],
        "description": request.form["description"],
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "id": request.form['id']
    }
    Car.update_car(data)
    return redirect('/dashboard')


@app.route('/delete/<int:id>')
def delete_car(id):
    if 'seller_id' not in session:
        return redirect('/logout')
    data = { "id":id}
    Car.delete(data)
    return redirect('/dashboard')




