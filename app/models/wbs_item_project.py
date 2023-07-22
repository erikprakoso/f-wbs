from app import db


class WbsItemProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    wbs_detail_project_id = db.Column(db.Integer, db.ForeignKey('wbs_detail_project.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<WbsItemProject {}>'.format(self.name)
    
    def to_dict(self):
        data = {
            'id': self.id,
            'wbs_detail_project_id': self.wbs_detail_project_id,
            'code': self.code,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return data
