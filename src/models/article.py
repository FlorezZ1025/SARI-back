from src.utils.db import db
from src.models.user import User
from sqlalchemy.dialects.postgresql import ARRAY

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.String(36), primary_key=True)
    id_user = db.Column(db.String(36), db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(ARRAY(db.String(255)), nullable=True)
    date = db.Column(db.String(255), nullable=True)
    hyperlink = db.Column(db.String(255), nullable=True)

    autores_objetos = db.relationship('Usuario',
                                   secondary='usuarios',  # Esto es un truco para la relación
                                   primaryjoin='Articulo.autores.contains(Usuario.id)',
                                   secondaryjoin='Usuario.id == Usuario.id',
                                   viewonly=True,
                                   lazy='dynamic')