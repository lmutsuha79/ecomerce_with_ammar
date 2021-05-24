from . import db, bcrypt
from flask_bcrypt import check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    _password = db.Column(db.String(), nullable=False)
    wallet = db.Column(db.Integer, nullable=False, default=1000)
    # items = db.relationship('Product', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LoginDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, default=datetime.now())

