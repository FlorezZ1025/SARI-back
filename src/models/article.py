from src.utils.db import db
from src.models.user import User
import json

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.String(36), primary_key=True)
    id_user = db.Column(db.String(36), db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(255), nullable=True)
    hyperlink = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=False)
    pdf_url = db.Column(db.String(500), nullable=True) 
    
    def insert_articles(self, email: str, articles: list):

        user = User.query.filter_by(email=email).first()

        Article.query.filter(
            Article.id_user == user.id,
            Article.state == 'publicado' ).delete()
        print('--------------')
        articles = [
            Article(
            id = article['id'],
            id_user = user.id,
            title = article['title'],
            authors = json.dumps(article['authors']),
            date = article['date'],
            hyperlink = article['hyperlink'],
            state = article['state'],
            )
            for article in articles
        ]
        db.session.add_all(articles)
        db.session.commit()