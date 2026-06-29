import logging
import os
from datetime import datetime

from flask import Flask, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
import markdown as md

from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"  # function name for login, this is called when we try to access a page restricted behind login
login_manager.login_message_category = "info"  # bootstrap class for flash messages to be displyed when trying to access restricted pages
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure DATA_DIR and profile_pictures dir exist
    os.makedirs(app.config["PROFILE_PICTURES_DIR"], exist_ok=True)

    # File logging - log file named by server start timestamp
    log_dir = Config.LOGS_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Server started")
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskblog.main.routes import main
    from flaskblog.posts.routes import posts
    from flaskblog.users.routes import users
    from flaskblog.errors.handlers import errors
    from flaskblog.admin.routes import admin
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(admin)

    @app.template_filter('markdown')
    def markdown_filter(text):
        return Markup(md.markdown(text, extensions=['fenced_code', 'tables']))

    @app.context_processor
    def inject_config():
        return dict(config=app.config)

    @app.route('/profile_pictures/<filename>')
    def profile_pic(filename):
        return send_from_directory(app.config["PROFILE_PICTURES_DIR"], filename)

    return app
