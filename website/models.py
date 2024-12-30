# create database models

# import from current package (. = website) the db object (SQLAlchemy())
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func # current date and time

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # match to id of user

# class Reminder(db.Model):
    
# class Video(db.Model):
    

# one-to-many relationship ... user with multiple notes
class User(db.Model, UserMixin):
    # unique identifier for primary key
    id = db.Column(db.Integer, primary_key=True)
    # max length of email 150....... no user can have same email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # reference name of class



