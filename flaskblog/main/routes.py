from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", newTitle="About")


@main.route("/api/home")
def api_home():
    posts = Post.query.order_by(Post.date_posted.desc())
    
    return {"posts": [post.to_dict() for post in posts]}

@main.route("/api/home/paginate/<int:page>")
def api_home_paginate(page):
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    return {"posts": [post.to_dict() for post in posts]}
    