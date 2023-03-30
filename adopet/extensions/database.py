import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)


class Caretaker(db.Model):
    __tablename__ = 'caretaker'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    about = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    password_hash = db.Column(db.String, nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_pwd(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"'id': {self.id}, 'name': {self.name}, 'email': {self.email}, 'phone': {self.phone}, 'city': {self.city}"
    
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'phone':self.phone,
            'city':self.city,
            'about':self.about,
            'photo':self.photo,
            'created_at':self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at':self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'deleted_at':self.deleted_at.strftime('%Y-%m-%d %H:%M:%S')
        } 

