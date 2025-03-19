from backend import db
from backend.models.prazo_model import Prazo
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

class PrazoService:
    
    @staticmethod
    def criar_prazo(titulo, setor_id, prazo):
        """Cria um novo prazo no banco de dados, validando os dados antes."""
        if not titulo or not setor_id or not prazo:
            raise ValueError("Todos os campos (título, setor e prazo) são obrigatórios!")

        try:
            novo_prazo = Prazo(titulo=titulo, setor_id=setor_id, prazo=prazo)
            db.session.add(novo_prazo)
            db.session.commit()
            return {"id": novo_prazo.id, "mensagem": "Prazo criado com sucesso!"}

        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erro ao criar prazo. Setor inexistente ou valor duplicado.")
    
    @staticmethod
    def listar_prazos():
        """Lista todos os prazos disponíveis."""
        prazos = Prazo.query.all()
        
        if not prazos:
            return []  # 🔥 Se não houver prazos, retorna uma lista vazia

        return [
            {
                "id": p.id,
                "titulo": p.titulo,
                "setor_id": p.setor_id,
                "prazo": PrazoService.formatar_prazo(p.prazo)
            }
            for p in prazos
        ]

    @staticmethod
    def buscar_prazo_por_id(prazo_id):
        """Busca um prazo específico pelo ID."""
        if not prazo_id:
            raise ValueError("O ID do prazo é obrigatório!")

        prazo = db.session.get(Prazo, prazo_id)

        if not prazo:
            raise ValueError("Prazo não encontrado!")

        return {
            "id": prazo.id,
            "titulo": prazo.titulo,
            "setor_id": prazo.setor_id,
            "prazo": PrazoService.formatar_prazo(prazo.prazo)
        }
    
    @staticmethod
    def deletar_prazo_por_id(prazo_id):
        """Deleta um prazo do banco de dados, garantindo que ele exista antes."""
        if not prazo_id:
            raise ValueError("O ID do prazo é obrigatório!")

        prazo = db.session.get(Prazo, prazo_id)

        if not prazo:
            raise ValueError("Prazo não encontrado!")

        db.session.delete(prazo)
        db.session.commit()

        return {"mensagem": "Prazo excluído com sucesso!"}

    @staticmethod
    def formatar_prazo(prazo):
        """Converte um timedelta ou string em um formato HH:MM:SS"""
        if isinstance(prazo, timedelta):
            total_segundos = int(prazo.total_seconds())
            horas, resto = divmod(total_segundos, 3600)
            minutos, segundos = divmod(resto, 60)
            return f"{horas:02}:{minutos:02}:{segundos:02}"
        return str(prazo)  # Caso já esteja formatado como string
