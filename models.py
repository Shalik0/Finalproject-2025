from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db, login_manager


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    img = db.Column(db.String(), nullable=False)
    link = db.Column(db.String(), nullable=True)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)