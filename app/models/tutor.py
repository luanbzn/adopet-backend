import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from ..extensions import db


class Tutor(db.Model):
    __tablename__ = 'tutor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    foto = db.Column(db.String, nullable=True)
    telefone = db.Column(db.String, nullable=True)
    municipio = db.Column(db.String, nullable=True)
    sobre = db.Column(db.String, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    pwd_hash = db.Column(db.String, nullable=False)

    @property
    def senha(self):
        raise AttributeError('Senha is not a readable attribute')

    @senha.setter
    def senha(self, senha):
        self.pwd_hash = generate_password_hash(senha)

    def verify_pwd(self, senha):
        return check_password_hash(self.pwd_hash, senha)

    def __repr__(self):
        return f"'id': {self.id}, 'nome': {self.nome}, 'email': {self.email}, 'telefone': {self.telefone}, 'municipio': {self.municipio}"

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'municipio': self.municipio,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }