from backend import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.String(36), primary_key=True)  # UUID como string
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    setor = db.relationship("Setor", backref=db.backref("usuarios", lazy=True))

    def __repr__(self):
        return f"<Usuario {self.nome}>"
    
    @staticmethod
    def hashing_pwd(senha):
        return generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
