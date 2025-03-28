from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime


"""
User class:
"""
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # Additional registration fields
    full_name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False, default="John Doe")
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)  # university email
    contact_number: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False, default="0000000000")
    time_zone: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False, default="GMT")
    diagnostics: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# New model to hold Emergency Contact details with a one-to-one relationship to User
"""
User has a 1..1 multiplicity association relationship with EmergencyContact, indicating each user has one emergency contact.
This has been shown in these classes with a user_id as primary key and the fact user_id is unique.
"""
class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    relationship = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    user = db.relationship("User", backref=db.backref("emergency_contact", uselist=False))

    def __repr__(self):
        return f"<EmergencyContact {self.full_name} for User {self.user_id}>"

# Existing MoodEntry model for daily data logging
class Mood_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)  # For prototype, assume a single user
    date = db.Column(db.Date, default=lambda: datetime.now().date())  # Only the date portion
    mood = db.Column(db.String(20), nullable=True)
    sentiment_score = db.Column(db.Float, nullable=True)
    smartwatch_data = db.Column(db.String(50), nullable=True)
    weather = db.Column(db.String(50), nullable=True)
    timetable = db.Column(db.String(50), nullable=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='unique_user_date'),)

    def __repr__(self):
        return f"<MoodEntry {self.date} - {self.mood}>"



