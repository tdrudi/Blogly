from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"


class Users(db.Model):
    """Users on website"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_URL) 

    posts = db.relationship("Posts", backref="user")

class Posts(db.Model):
    """Posts"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    post_content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 


def connect_db(app):
    """Connect to database"""
    db.app = app    
    db.init_app(app)
