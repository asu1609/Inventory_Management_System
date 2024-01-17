from flask import *
from my_app import app, db
from my_app.forms import Productform, Locationform, ProductMovementform
from my_app.models.product import Product
from my_app.models.location import Location
from my_app.models.productmovement import ProductMovement
from my_app.models.stock import Stock


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/product', methods=['GET','POST'])
def product():
    form = Productform()
    product = Product()
    columns = Product.__table__.columns.keys()
    products = product.display_product()

    if form.validate_on_submit():
        print(form.product_name.data)
        product.create_product(form)
        return redirect(url_for('product'))
    
    return render_template('product.html',columns=columns, form=form, products = products, page = 'Product')


@app.route('/location', methods = ['GET', 'POST'])
def location():
    form = Locationform()
    location = Location()
    columns = Location.__table__.columns.keys()
    locations = location.display_location()

    if form.validate_on_submit():
        location.create_location(form)
        return redirect(url_for('location'))
    
    return render_template('location.html',columns=columns, form=form, locations = locations, page = 'Location')


@app.route('/product_movement', methods = ['GET', 'POST'])
def product_movement():
    form = ProductMovementform()
    movement = ProductMovement()
    location = Location()
    product = Product()
    columns = ProductMovement.__table__.columns.keys()  
    movements = movement.display_movements()
    locations = location.display_location()
    products = product.display_product()

    if request.method == 'POST':
        if form.validate_on_submit() or movement.check(form):
            movement.check_movement(form)
            return redirect(url_for('product_movement'))
        else:
            flash("Enter any one location.")
            return redirect(url_for('product_movement'))
    
    return render_template('product_movement.html', form=form, movements= movements, locations = locations, products = products, page = 'Movement', columns = columns)



@app.route('/update_product/<int:product_id>', methods = ['GET', 'POST'])
def update_product(product_id):
    form = Productform()
    product = Product()

    if request.method == 'POST' and form.validate_on_submit():
        product.update_product(product_id, form)
        return redirect(url_for('product'))


@app.route('/update_location/<int:location_id>', methods = ['GET','POST'])
def update_location(location_id):
    form = Locationform()
    location = Location()

    if request.method == 'POST' and form.validate_on_submit():
        print(form.location_name.data)
        location.update_location(location_id,form)
        return redirect(url_for('location'))


@app.route('/update_movement/<int:movement_id>', methods = ['GET', 'POST'])
def update_movement(movement_id):
    form = ProductMovementform()
    movement = ProductMovement()

    data = ProductMovement.query.filter_by(id = movement_id).first()
    
    if request.method == 'POST'and form.validate_on_submit() and movement.check(form):
        movement.update_movement(form, data)
        return redirect(url_for('product_movement'))
    

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    product = Product()
    product.delete_product(product_id)

    return redirect(url_for('product'))


@app.route('/delete_location/<int:location_id>')
def delete_location(location_id):
    location = Location()
    location.delete_location(location_id)

    return redirect(url_for('location'))


@app.route('/delete_movement/<int:movement_id>')
def delete_movement(movement_id):
    movement = ProductMovement()
    movement.delete_movement(movement_id)

    return redirect(url_for('product_movement'))

@app.route('/report', methods = ['GET'])
def report():
    product_count = Product.query.count()
    location_count = Location.query.count()
    return render_template('report.html', product_count = product_count, location_count = location_count)

@app.route('/product_details', methods = ['POST','GET'])
def product_details():
    distinct_locations = db.session.query(Stock.location_name).distinct().all()
    if request.method == 'POST':
        selected_location = request.form.get('locations')
        product = Stock.query.filter_by(location_name = selected_location)
        return render_template('product_details.html', location = distinct_locations, product = product, selected_location = selected_location)
    
    return render_template('product_details.html', location = distinct_locations)

@app.route('/location_details', methods = ['GET','POST'])
def location_details():
    distinct_products = db.session.query(Stock.product_name).distinct().all()
    locations = db.session.query(Stock.location_name, db.func.sum(Stock.quantity)).group_by(Stock.location_name).all()
    if request.method == 'POST':
        selected_product = request.form.get('products')
        product_stock = Stock.query.filter_by(product_name = selected_product).all()
        return render_template('location_details.html', locations = locations, products = distinct_products, product_stock = product_stock, selected_product = selected_product)
    
    return render_template('location_details.html', locations = locations, products = distinct_products)
    
    