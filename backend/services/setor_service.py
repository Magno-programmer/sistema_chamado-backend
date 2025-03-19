from backend import db
from backend.models.setor_model import Setor
from sqlalchemy.exc import IntegrityError

class SetorService:
    
    @staticmethod
    def listar_setores():
        """Lista todos os setores"""
        setores = Setor.query.all()
                    # 🔹 Converte os resultados (tuplas) para dicionários
        return [
            {
                "id": setor.id,
                "nome": setor.nome
            }
            for setor in setores
        ]

    @staticmethod
    def criar_setor(nome):
        """Cria um novo setor no banco de dados"""
        novo_setor = Setor(nome=nome)

        try:
            db.session.add(novo_setor)
            db.session.commit()
            return novo_setor.id
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erro ao criar setor. Nome já existente ou inválido.")

    @staticmethod
    def setor_tem_usuarios(setor_id):
        """Verifica se existem usuários vinculados ao setor"""
        from backend.models.usuario_model import Usuario  # Importação dentro do método para evitar circular import
        
        usuarios_no_setor = Usuario.query.filter_by(setor_id=setor_id).count()
        return usuarios_no_setor > 0  # Retorna True se houver usuários no setor

    @staticmethod
    def setor_tem_chamados(setor_id):
        """Verifica se existem chamados vinculados ao setor"""
        from backend.models.chamado_model import Chamado  # Importação dentro do método para evitar circular import

        chamados_no_setor = Chamado.query.filter_by(setor_id=setor_id).count()
        return chamados_no_setor > 0  # Retorna True se houver chamados no setor

    @staticmethod
    def deletar_setor(setor_id):
        """Exclui um setor do banco se ele não tiver usuários ou chamados vinculados"""
        setor = db.session.get(Setor, setor_id)
        if not setor:
            raise ValueError("Setor não encontrado.")

        if SetorService.setor_tem_usuarios(setor_id):
            raise ValueError("Setor possui usuários vinculados e não pode ser excluído.")

        if SetorService.setor_tem_chamados(setor_id):
            raise ValueError("Setor possui chamados vinculados e não pode ser excluído.")

        db.session.delete(setor)
        db.session.commit()
