from my_app import db
from flask_sqlalchemy import SQLAlchemy
from flask import flash


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'),nullable = False)
    location_name = db.Column(db.String(45), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    product_name = db.Column(db.String(45), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    product = db.relationship('Product',backref='stocks')
    location = db.relationship('Location',backref='stocks')

    def create_stock(self,location,product_name,quantity):
        from .product import Product
        product = Product.query.filter_by(product_name=product_name).first()
        from .location import Location
        l = Location.query.filter_by(location_name = location).first()
        new_stock = Stock(location_id = l.id,
                          location_name =  location, 
                          product_id = product.id,
                          product_name = product_name, 
                          quantity = quantity)
        db.session.add(new_stock)
        db.session.commit()
        flash('Stock added successfully.')

    def add_stock(self, location, product, quantity):
        stock = Stock.query.filter_by(location_name=location, product_name = product).first()
        if stock is None:
            self.create_stock(location, product, quantity)
        else:
            stock.quantity = stock.quantity + quantity
            db.session.commit()

    def remove_stock(self,location,product,quantity):
        stock = Stock.query.filter_by(location_name=location, product_name = product).first()
        if stock.quantity <= quantity :
            db.session.delete(stock)
        else:
            stock.quantity = stock.quantity - quantity
        db.session.commit()
        
    def check_stock_from(self,location,product,quantity):
        stock = Stock.query.filter_by(location_name=location, product_name = product).first()

        if stock is None or stock.quantity<quantity:
           flash('Out of stock.')
           return False
        else:
           self.remove_stock(location,product,quantity)
           return True
        
    def check_stock_to(self,location,product,quantity):
        stock = Stock.query.filter_by(location_name=location, product_name = product).first()

        if stock:
            self.add_stock(location,product,quantity)
        else:
            self.create_stock(location,product,quantity)