from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"


class User(db.Model):
    """Users on website"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_URL) 

    posts = db.relationship("Post", backref="user")

class Post(db.Model):
    """Posts"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    post_content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) 

class Tag(db.Model):
    """Tags"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False, unique = True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

class PostsTag(db.Model):
    """Tags added to posts"""
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


def connect_db(app):
    """Connect database to flask app"""
    db.app = app    
    db.init_app(app)
