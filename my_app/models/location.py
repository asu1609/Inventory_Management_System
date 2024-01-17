from my_app import db
from sqlalchemy.exc import IntegrityError
from flask import *

class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    location_name = db.Column(db.String(30), unique=True)
    address = db.Column(db.Text)

    def location_exist(self,name):
        print(self)
        result = Location.query.filter_by(location_name = name).first()
        if result:
            return True
        else:
            return False
    
    def create_location(self, location):
        try:
            new_location = Location(
                location_name = location.location_name.data, 
                address =  location.address.data)
            db.session.add(new_location)
            db.session.commit()
            flash('Location created successfully.')
        except IntegrityError:
            flash('Location already exist.')

    def display_location(self):
        locations = Location.query.all()
        return locations
    
    def update_location(self,location_id,form):
        location = Location.query.filter_by(id = location_id).first()
        if self.location_exist(location.location_name):
            from .stock import Stock
            stocks = Stock.query.filter_by(location_id = location_id).all()
            from .productmovement import ProductMovement
            movements1 = ProductMovement.query.filter_by(from_location = location.location_name).all()
            movements2 = ProductMovement.query.filter_by(to_location = location.location_name).all()
            location.location_name = form.location_name.data
            location.address = form.address.data
            for stock in stocks:
                stock.location_name = form.location_name.data
            for movement in movements1:
                movement.from_location = form.location_name.data
            for movement in movements2:
                movement.to_location = form.location_name.data
            flash("Updated Successfully.")
            db.session.commit()
    
    def delete_location(self, location_id):
        locations = Location.query.filter_by(id = location_id).first()
        from .stock import Stock
        Stock.query.filter_by(location_id = location_id).delete()
        db.session.delete(locations)
        db.session.commit()

column_location = Location.__table__.columns.keys()