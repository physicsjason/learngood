from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_mail import Message
from . import db, mail

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route("/test_email")
def test_email():
    msg = Message(subject='blueprint!',\
                  sender='learngood@jrltutors.com',\
                  recipients=['jason.leonard@gmail.com'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    #mail.send(msg)
    return "Message sent!"