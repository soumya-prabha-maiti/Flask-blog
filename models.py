from datetime import datetime
from __main__ import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(128),unique=True,nullable=False)
    # The profile pic may not be unique eg the default starting picture 
    profilePic=db.Column(db.String(20),nullable=False,default="default.jpg")
    password=db.Column(db.String(60),nullable=False)

    # A relationship is not a column , but actually it runs a query in the on the post table
    # backref = 
    # lazy = 
    posts=db.relationship('Post',backref='author',lazy=True)

    def ___repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"
    
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    datePosted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    userId=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    # The argument of ForeignKey is small letter user since it represents the table user
    # For every class, the corresponding table is small lettered by default

    def ___repr__(self):
        return f"User('{self.title}','{self.datePosted}')"
