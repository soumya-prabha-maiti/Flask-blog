import os
import secrets
from flask import url_for,current_app
from flask_mail import Message
from flaskblog import mail
from PIL import Image


def save_profile_pic(form_profile_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_profile_pic.filename)
    profile_pic_filename = random_hex+f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pictures', profile_pic_filename)

    output_size = (256, 256)
    i = Image.open(form_profile_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return profile_pic_filename


def send_reset_email(user):
    token = user.create_pw_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    
{url_for('users.reset_password',token=token,_external=True)}

If you did not make this request, you can safely ignore this email and no changes will be made to your accout.
    '''
    mail.send(msg)
