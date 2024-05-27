"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
with app.app_context():db.create_all()
@app.route("/", methods = ["GET"])
def home_page():

    users = User.query.all()

    return render_template("home.html", users = users)

@app.route("/create")
def add_user_form():
    
    return render_template ('add_update.html', form = 'create') 

@app.route("/update/<int:user_id>")
def update_user_form(user_id):
    


    return render_template ('add_update.html', form = 'update', user_id = user_id )

@app.route("/users/posts/<int:user_id>/create")
def add_post_form(user_id):
    
    return render_template ('add_update_posts.html', form = 'create', user_id = user_id) 

@app.route("/users/posts/update/<int:post_id>")
def update_post_form( post_id):
    


    return render_template ('add_update_posts.html', form = 'update', post_id = post_id)

@app.route('/', methods = ["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    photo_url = request.form["photo_url"]

    user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], image_url=request.form["photo_url"])
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")

@app.route('/update/<int:user_id>', methods = ["POST"])
def update_user(user_id):
    current_user = User.query.get_or_404(user_id)
    current_user.first_name = request.form["first_name"]
    current_user.last_name = request.form["last_name"]
    current_user.image_url = request.form["photo_url"]


    db.session.add(current_user)
    db.session.commit()

    return redirect(f"/{user_id}")

@app.route('/delete/<int:user_id>', methods = ["POST"])
def delete_user(user_id):
    current_user = User.query.get_or_404(user_id)

    db.session.delete(current_user)
    db.session.commit()

    return redirect("/")

@app.route("/<int:user_id>")
def show_user(user_id):
    current_user = User.query.get_or_404(user_id)
    first_name = current_user.first_name
    last_name = current_user.last_name
    picture = current_user.image_url
    posts = Post.query.filter(Post.created_by== user_id)

    return render_template("user.html", first_name = first_name, last_name = last_name, picture = picture, user_id = current_user.id, posts=posts)

@app.route("/users/posts/<int:user_id>/create", methods = ["POST"])
def create_post(user_id):

    title = request.form["title"]
    content = request.form['content']
    created_at = datetime.now()
    created_by = user_id

    post = Post(title= title, content = content, created_at = created_at, created_by = created_by)

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/posts/{post.id}")

@app.route('/users/posts/<int:post_id>')
def display_post(post_id):

    post = Post.query.get_or_404(post_id)
    title = post.title
    content = post.content
    created_at = post.created_at
    created_by = post.user.first_name+" "+post.user.last_name

    return render_template('posts.html', title = title, content = content, created_at = created_at, created_by= created_by, post_id = post_id)

@app.route('/users/posts/update/<int:post_id>', methods = ["POST"])
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/posts/{post_id}')
    
@app.route('/users/posts/delete/<int:post_id>', methods = ["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/")