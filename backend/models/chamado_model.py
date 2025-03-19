from backend import db

class Chamado(db.Model):
    __tablename__ = "chamados"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    solicitante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Aberto")
    prazo = db.Column(db.Interval, nullable=False)  # 🔥 Armazena como INTERVAL no banco

    # Relacionamentos
    setor = db.relationship("Setor", backref="chamados")
    solicitante = db.relationship("Usuario", foreign_keys=[solicitante_id])
    responsavel = db.relationship("Usuario", foreign_keys=[responsavel_id])

    def __repr__(self):
        return f"<Chamado {self.titulo} - {self.status}>"
