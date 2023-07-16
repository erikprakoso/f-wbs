from app import db
from datetime import datetime

class WbsHeader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    wbs_details = db.relationship('WbsDetail', backref='wbs_header', lazy=True, cascade='all, delete-orphan')