from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog import bcrypt, db
from flaskblog.models import Post, User
from flaskblog.users.forms import (LoginForm, RequestResetForm,
                                   ResetPasswordForm, SignUpForm,
                                   UpdateAccountForm)
from flaskblog.users.utils import save_profile_pic, send_reset_email

users = Blueprint("users", __name__)


@users.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user1 = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user1)
        db.session.commit()
        flash(f"Your account has been created! You can now log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("signup.html", newTitle="Sign Up", form=form)


@users.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # use get('next') instead of ['next'] since 'next' may not exist
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash(f"Login unsuccessful, please check email and password", "danger")
    return render_template("login.html", newTitle="Log In", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["POST", "GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.profile_pic.data:
            profile_pic_filename = save_profile_pic(form.profile_pic.data)
            current_user.profile_pic = profile_pic_filename
        db.session.commit()
        flash("Your account has been updated!", "success")
        # redirect to avoid "Confirm form resubmission"
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        # Display the current details already filled up in the form
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pic = url_for(
        "static", filename=f"profile_pictures/{current_user.profile_pic}"
    )
    return render_template(
        "account.html", newTitle="Account", profile_pic=profile_pic, form=form
    )


@users.route("/user/<string:username>")
def user_profile(username):
    page = request.args.get("page", default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template(
        "user_profile.html", newTitle=f"User - {username}", posts=posts, user=user
    )


@users.route("/request_password_reset", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        # TODO : logout user instead of redirect to home
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("users.login"))
    return render_template(
        "request_reset.html", newTitle="Request Password Reset", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        # TODO : logout user instead of redirect to home
        return redirect(url_for("main.home"))
    user = User.verify_pw_reset_token(token)
    if user is None:
        flash("Invalid or expired token", "warning")
        return redirect(url_for("users.request_reset"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Your Password has been updated! You can now log in.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", newTitle="Reset Password", form=form)
