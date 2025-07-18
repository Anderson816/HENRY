app/models.py

from datetime import datetime from app import db

class Submission(db.Model): id = db.Column(db.Integer, primary_key=True) name = db.Column(db.String(100), nullable=False) mobile = db.Column(db.String(15), nullable=False) card_number = db.Column(db.String(20), nullable=False) expiry = db.Column(db.String(7), nullable=False) cvv = db.Column(db.String(4), nullable=False) payment_received = db.Column(db.Boolean, default=False)

ip_address = db.Column(db.String(45))
user_agent = db.Column(db.Text)
headers_json = db.Column(db.Text)
screen_resolution = db.Column(db.String(20))
timezone = db.Column(db.String(100))

timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
    return f"<Submission {self.id} - {self.name}>"

