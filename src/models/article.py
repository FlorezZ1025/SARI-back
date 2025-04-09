import uuid
from utils.db import db
from models.user import User
from sqlalchemy.dialects.postgresql import ARRAY

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user = db.Column(db.String(36), db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(255), nullable=True)
    hyperlink = db.Column(db.String(255), nullable=True)

    autores_objetos = db.relationship('Usuario',
                                   secondary='usuarios',  # Esto es un truco para la relación
                                   primaryjoin='Articulo.autores.contains(Usuario.id)',
                                   secondaryjoin='Usuario.id == Usuario.id',
                                   viewonly=True,
                                   lazy='dynamic')
    
    def insert_articles(self, email: str, articles: list):

        user = User.query.filter_by(email=email).first()

        Article.query.filter_by(id_user=user.id).delete()

        articles = [
            Article(
            id_user=user.id,
            title=article['title'],
            authors=article['authors'],
            date=article['date'],
            hyperlink=article['hyperlink']
            )
            for article in articles
        ]
        db.session.add_all(articles)
        db.session.commit()