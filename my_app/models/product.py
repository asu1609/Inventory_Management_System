from my_app import db
from sqlalchemy.exc import IntegrityError
from flask import *
from .stock import Stock
from .productmovement import ProductMovement

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    product_name = db.Column(db.String(30), unique = True)
    brand_name = db.Column(db.String(30))
    price = db.Column(db.Integer)
    productmovement = db.relationship('ProductMovement', backref='product', cascade = 'all, delete')

    def product_exist(self, name):
        result = Product.query.filter_by(product_name = name).first()
        if result:
            return True
        else:
            return False
        
    def create_product(self, product):
        try:
            new_product = Product(
                    product_name = product.product_name.data, 
                    brand_name =  product.brand_name.data, 
                    price = product.price.data)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully.')
        except IntegrityError:
            flash('Product already exist.')

    def display_product(self):
        products = Product.query.all()
        return products
    
    def update_product(self, product_id, form):
        update_product = Product.query.filter_by(id=product_id).first()
        update_product.product_name = form.product_name.data
        update_product.brand_name = form.brand_name.data
        update_product.price = form.price.data
        stocks = Stock.query.filter_by(product_id = product_id).all()
        movements = ProductMovement.query.filter_by(product_id = product_id).all()
        for stock in stocks:
            stock.product_name = form.product_name.data
        for movement in movements:
            movement.product_name = form.product_name.data

        db.session.commit()

    def delete_product(self, product_id):
        products = Product.query.filter_by(id = product_id).first()
        Stock.query.filter_by(product_id = product_id).delete()
        db.session.delete(products)
        db.session.commit()

column_product = Product.__table__.columns.keys()