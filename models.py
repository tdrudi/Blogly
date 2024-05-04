from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

"""Models for Blogly."""
class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_URL) 

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)
