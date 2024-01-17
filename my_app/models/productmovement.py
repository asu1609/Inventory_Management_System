from my_app import db
from sqlalchemy.exc import IntegrityError
from flask import *
from datetime import datetime

class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    from_location = db.Column(db.String(30))
    to_location = db.Column(db.String(30))
    time_stamp = db.Column(db.DateTime)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(30))
    quantity = db.Column(db.Integer)

    def check(self, form):
        if form.from_location.data or form.to_location.data :
            return True
        else :
            return False

    def check_movement(self,movement):
        from .location import Location
        location = Location()
        from .product import Product
        product = Product()
        from .stock import Stock
        stock = Stock()

        if movement.from_location.data and movement.product_name.data and movement.to_location.data == '':
            fl = location.location_exist(movement.from_location.data)
            p = product.product_exist(movement.product_name.data)
            if fl and p and stock.check_stock_from(movement.from_location.data, movement.product_name.data, movement.quantity.data):
                self.create_movement(movement)
            elif fl:
                flash('Product does not exist.')
            else:
                flash('From Location does not exist.')

        if movement.to_location.data and movement.product_name.data and movement.from_location.data == '':
            tl = location.location_exist(movement.to_location.data)
            p = product.product_exist(movement.product_name.data)
            if tl and p:
                stock.check_stock_to(movement.to_location.data, movement.product_name.data, movement.quantity.data)
                self.create_movement(movement)
            else:
                if tl:
                    flash('Product does not exist.')
                else:
                    flash('To Location does not exist.')

        if movement.from_location.data and movement.product_name.data and movement.to_location.data:
            fl = location.location_exist(movement.from_location.data)
            tl = location.location_exist(movement.to_location.data)
            p = product.product_exist(movement.product_name.data)
            if fl and tl and p and stock.check_stock_from(movement.from_location.data, movement.product_name.data, movement.quantity.data) :
                stock.check_stock_to(movement.to_location.data, movement.product_name.data, movement.quantity.data)
                self.create_movement(movement)  
            else:
                if not tl:
                    flash('To Location does not exist.')
                if not fl:
                    flash('From Location does not exist.')
                if not p:
                    flash('Product does not exist.')

    def create_movement(self, movement):
        new_movement = ProductMovement(
                from_location = movement.from_location.data, 
                to_location =  movement.to_location.data, 
                time_stamp = datetime.now(),
                product_id = self.get_product(movement.product_name.data).id,
                product_name = self.get_product(movement.product_name.data).product_name,
                quantity = movement.quantity.data)
        db.session.add(new_movement)
        db.session.commit()
        flash('Movement added successfully.')

    def display_movements(self):
        movements = ProductMovement.query.all()
        return movements
        
    def get_product(self,product_name):
        from .product import Product
        product = Product.query.filter_by(product_name=product_name).first()
        return product

    def compare(self,old, new):
        if old == new:
            return False
        else :
            return True
        
    def delete_movement(self,movement_id):
        from .stock import Stock
        stock = Stock()
        delete_movement = ProductMovement.query.filter_by(id = movement_id).first()
        if delete_movement.from_location:
            stock.add_stock(delete_movement.from_location, delete_movement.product_name, delete_movement.quantity)
        if delete_movement.to_location:
            stock.remove_stock(delete_movement.to_location, delete_movement.product_name, delete_movement.quantity)
    
        db.session.delete(delete_movement)
        db.session.commit()

    def update_movement(self,new_movement,old_movement):
        self.delete_movement(old_movement.id)
        self.check_movement(new_movement)

column_productMovement = ProductMovement.__table__.columns.keys()