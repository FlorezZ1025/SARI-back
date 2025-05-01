from utils.db import db
from models.user import User
import json

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.String(36), primary_key=True)
    id_user = db.Column(db.String(36), db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=False)

    def insert_porjects(self, email: str, projects: list):
        user = User.query.filter_by(email=email).first()

        Project.query.filter(
            Project.id_user == user.id,
            Project.state == 'publicado').delete()

        projects = [
            Project(
                id=project['id'],
                id_user=user.id,
                title=project['title'],
                date=project['date'],
                state=project['state'],
            )
            for project in projects
        ]
        db.session.add_all(projects)
        db.session.commit()
