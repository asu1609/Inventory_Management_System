from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class Productform (FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    brand_name = StringField('Brand Name', validators=[DataRequired()])
    price = IntegerField('Price (in INR)', validators=[DataRequired(), NumberRange(min=1)])
    add = SubmitField('Add')
    update = SubmitField('Update')

class Locationform (FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    add = SubmitField('Add')
    update = SubmitField('Update')

class ProductMovementform (FlaskForm):
    from_location = StringField('From Location')
    to_location = StringField('To Location')
    product_name = StringField('Product Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    add = SubmitField('Add')
    update = SubmitField('update')