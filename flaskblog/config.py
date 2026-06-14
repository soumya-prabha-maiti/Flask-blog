import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.path.abspath(os.environ["DATA_DIR"])


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DATA_DIR, 'site.db')}"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    PROFILE_PICTURES_DIR = os.path.join(DATA_DIR, "profile_pictures")
