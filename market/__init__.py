from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CSRFProtect

SECRET_KEY = b'9\x95\x83\x97\xb0;\xa1\xb2k\xae6\x0e\x00\xb8\xf4\x8a\x03*\xcf\xb6\xcc\x94 L\xbe\xef\xbc\x85\x96ol\xb5'

app = Flask(__name__, template_folder=r'..\templates', static_folder=r'..\static')

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///..\dbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app=app)
login_manager.login_view = '/login'

from market import route
