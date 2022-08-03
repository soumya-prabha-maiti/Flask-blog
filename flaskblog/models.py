from datetime import datetime,timedelta,timezone
import jwt
from flaskblog import db, login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
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

    def create_pw_reset_token(self,expires_sec=120):
        reset_token = jwt.encode(
                {
                    "user_id": self.id,
                    "exp": datetime.now(tz=timezone.utc)
                        + timedelta(seconds=expires_sec)

                },
                app.config['SECRET_KEY'],
                algorithm="HS256"
            )
        return reset_token

    @staticmethod
    def verify_pw_reset_token(token):
        try:
            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )
            user_id=data['user_id']
        except:
            return None
        return User.query.get(user_id)
            
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"
    
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    datePosted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    userId=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    # The argument of ForeignKey is small letter user since it represents the table user
    # For every class, the corresponding table is small lettered by default

    def __repr__(self):
        return f"Post('{self.title}','{self.datePosted}')"

    

