"""Models for Blogly."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy



db= SQLAlchemy()

class User (db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
    first_name = db.Column(db.String(15),
                        nullable = False,
                        unique = True)
    last_name = db.Column(db.String(15),
                        nullable = False,
                        unique = True)
    image_url = db.Column(db.String(),
                          default = "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg")



def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

