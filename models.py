from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    sentence_threshold = db.Column(db.Float, default=0.75)
    pair_threshold = db.Column(db.Float, default=60.0)
    failed_logins = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Null for global demo docs
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CheckHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # Single, Batch, Cross
    title = db.Column(db.String(200), nullable=True)
    text = db.Column(db.Text, nullable=True) # The checked text or file list
    score = db.Column(db.Float, nullable=True)
    details = db.Column(db.Text, nullable=True) # JSON details
    date = db.Column(db.DateTime, default=datetime.utcnow)

