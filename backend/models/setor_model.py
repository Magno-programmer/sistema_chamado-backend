from backend import db

class Setor(db.Model):
    __tablename__ = "setores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Setor {self.nome}>"
