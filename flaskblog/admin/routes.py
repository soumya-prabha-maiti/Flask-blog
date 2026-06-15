from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, abort, current_app, render_template
from flask_login import current_user, login_required

from flaskblog import db
from flaskblog.models import Post, User

admin = Blueprint("admin", __name__)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.email not in current_app.config["ADMIN_EMAILS"]:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin.route("/admin")
@admin_required
def dashboard():
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)

    total_users = User.query.count()
    total_posts = Post.query.count()
    posts_this_week = Post.query.filter(Post.date_posted >= week_ago).count()
    recent_users = User.query.order_by(User.id.desc()).limit(5).all()
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    top_authors = (
        db.session.query(User.username, db.func.count(Post.id).label("post_count"))
        .join(Post)
        .group_by(User.id)
        .order_by(db.func.count(Post.id).desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin.html",
        newTitle="Admin",
        total_users=total_users,
        total_posts=total_posts,
        posts_this_week=posts_this_week,
        recent_users=recent_users,
        recent_posts=recent_posts,
        top_authors=top_authors,
    )
