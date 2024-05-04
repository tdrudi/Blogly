"""Blogly application."""
from flask import Flask, render_template, request, redirect
from models import db, connect_db, Users, Posts

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'key123'

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def homepage():
    """Redirect to list of users"""
    return redirect("/users")

@app.route("/users")
def show_all_users():
    """Show all users"""
    users = Users.query.all()
    return render_template("all_users.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    """Form for new users"""
    return render_template("new_user.html")

@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Process add form, add new user and go back to /users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = Users(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Show info about user, have button to get to edit 
    page and to delete user"""
    user = Users.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def user_edit_page(user_id):
    """Show edit page for user, cancel button to return to 
    detail page and save button to save updates"""
    user = Users.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods={"POST"})
def edit_user_info(user_id):
    """Edit form and return to /users page"""
    user = Users.query.get_or_404(user_id)
    
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """delete user"""
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Form to add post for user"""
    user = Users.query.get_or_404(user_id)
    return render_template("create_post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Get post form info, add post, redirect to user details page"""
    user = Users.query.get_or_404(user_id)
    title = request.form["title"]
    post_content = request.form["post_content"]
    new_post = Posts(title=title, post_content=post_content, user=user)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a post, buttons to edit and delete"""
    post = Posts.query.get_or_404(post_id)
    return render_template("show_post.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Form to edit post and cancel/back to user page"""
    post = Posts.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods={"POST"})
def save_edit_post(post_id):
    """Handle post edit, redirect back to post view"""
    post = Posts.query.get_or_404(post_id)
    post.title = request.form['title']
    post.post_content = request.form['post_content']

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Posts.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')