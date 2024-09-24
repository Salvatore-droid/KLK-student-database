from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['SECRET_KEY'] = '04464596c1d26d25713399e96466b35e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from klk import routes

with app.app_context():
    db.create_all()

