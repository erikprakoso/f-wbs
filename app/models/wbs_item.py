from app import db
from datetime import datetime

class WbsItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wbs_detail_id = db.Column(db.Integer, db.ForeignKey('wbs_detail.id'), nullable=False)
    code = db.Column(db.String(255))
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)