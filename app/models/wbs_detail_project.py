from app import db


class WbsDetailProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    wbs_header_project_id = db.Column(db.Integer, db.ForeignKey('wbs_header_project.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    wbs_items = db.relationship('WbsItemProject', backref='wbs_detail_project', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return '<WbsDetailProject {}>'.format(self.name)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'wbs_header_project_id': self.wbs_header_project_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'wbs_items': [wbs_item.to_dict() for wbs_item in self.wbs_items]
        }
        return data