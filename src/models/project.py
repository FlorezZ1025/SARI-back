from src.utils.db import db
from src.models.user import User
import json

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.String(36), primary_key=True)
    id_user = db.Column(db.String(36), db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    investigators = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=False)
    pdf_url = db.Column(db.String(500), nullable=True)

    def insert_projects(self, email: str, projects: list):
        user = User.query.filter_by(email=email).first()

        Project.query.filter(
            Project.id_user == user.id,
            Project.status == 'Finalizado').delete()

        projects = [
            Project(
                id=project['id'],
                id_user=user.id,
                title=project['title'],
                investigators=json.dumps(project['investigators']),
                date=project['date'],
                status=project['status'],
            )
            for project in projects
        ]
        db.session.add_all(projects)
        db.session.commit()
