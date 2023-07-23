from app import db


class WbsHeaderProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)
    
    wbs_details = db.relationship('WbsDetailProject', backref='wbs_header_project', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return '<WbsHeaderProject {}>'.format(self.name)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'wbs_details': [wbs_detail.to_dict() for wbs_detail in self.wbs_details]
        }
        return data