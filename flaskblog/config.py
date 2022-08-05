import os
import json

with open("/etc/flask_blog_config.json",) as config_file:
    config=json.load(config_file)


class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")  # //// used for absolute path; ///used for relative path with respect to the project folder
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get("EMAIL_USERNAME")
    MAIL_PASSWORD = config.get("EMAIL_PASSWORD")
