from backend import db

class Prazo(db.Model):
    __tablename__ = "prazos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    prazo = db.Column(db.Interval, nullable=False)  # 🔥 Armazena como INTERVAL no banco

    def __repr__(self):
        return f"<Prazo {self.titulo} - {self.prazo}>"
