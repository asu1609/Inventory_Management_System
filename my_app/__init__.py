from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456789@localhost:3306/ims'
app.config['SECRET_KEY'] = 'hard to guess string'
db = SQLAlchemy(app)

from my_app import routes, models
with app.app_context():
    db.create_all()

