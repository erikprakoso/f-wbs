from app import db

class SheetName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))