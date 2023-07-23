from app import db
from datetime import datetime

class WbsDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wbs_header_id = db.Column(db.Integer, db.ForeignKey('wbs_header.id'), nullable=False)
    code = db.Column(db.String(255))
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    wbs_items = db.relationship('WbsItem', backref='wbs_detail', lazy=True, cascade='all, delete-orphan')