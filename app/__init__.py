from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_login import login_user
import os

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import views, models

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, generate_password_hash=generate_password_hash)


def create_sample_user():
    from app.models import User, EmergencyContact
    if User.query.count() == 0:
        # Create a sample user with hardcoded registration details
        user = User(
            full_name="Alice Smith",
            username="alice",
            email="alice@university.edu",
            contact_number="1234567890",
            time_zone="GMT",
            diagnostics="None"
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        # Create the associated emergency contact record
        ec = EmergencyContact(
            user_id=user.id,
            full_name="Bob Smith",
            relationship="Father",
            email="bob@contact.com",
            contact_number="0987654321"
        )
        db.session.add(ec)
        db.session.commit()

# Seed the database using the application context
with app.app_context():
    db.create_all()
    create_sample_user()