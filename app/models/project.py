from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    location = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    revit_file = db.Column(db.String(255))
    excel_file = db.Column(db.String(255))
    photo_file = db.Column(db.String(255))
    sheet_names = db.relationship('SheetName', backref='project', lazy=True)