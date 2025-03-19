from backend import db
from backend.models.chamado_model import Chamado
from backend.models.usuario_model import Usuario
from backend.models.setor_model import Setor
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased

class ChamadoService:
    
    @staticmethod
    def criar_chamado(titulo, descricao, solicitante_id, setor_id, prazo):
        """Cria um novo chamado no banco de dados, validando o setor e atribuindo responsável"""
        
        # 🚀 Valida se o setor existe antes de criar o chamado
        setor = db.session.get(Setor, setor_id)
        if not setor:
            raise ValueError("Setor inválido! O setor especificado não existe.")
        
        # 🚀 Seleciona o responsável com menos chamados abertos no setor
        responsavel_id = ChamadoService.selecionar_responsavel(setor_id)
        if not responsavel_id:
            raise ValueError("Nenhum responsável disponível para este setor!")

        try:
            novo_chamado = Chamado(
                titulo=titulo,
                descricao=descricao,
                solicitante_id=solicitante_id,
                setor_id=setor_id,
                responsavel_id=responsavel_id,
                status="Aberto",
                prazo=prazo
            )
            db.session.add(novo_chamado)
            db.session.commit()
            return {"id": novo_chamado.id, "mensagem": "Chamado criado com sucesso!"}

        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erro ao criar chamado. Verifique os dados e tente novamente.")
    
    @staticmethod
    def selecionar_responsavel(setor_id):
        """Seleciona o usuário do setor com menos chamados em aberto"""
        
        responsavel = (
            db.session.query(Usuario.id)
            .outerjoin(Chamado, (Usuario.id == Chamado.responsavel_id) & (Chamado.status == "Aberto"))
            .filter(Usuario.setor_id == setor_id)
            .group_by(Usuario.id)
            .order_by(db.func.count(Chamado.id).asc())
            .limit(1)
            .scalar()
        )

        return responsavel  # Retorna o ID do usuário com menos chamados abertos
    
    @staticmethod
    def atualizar_status(chamado_id, status):
        """Atualiza o status de um chamado"""
        
        chamado = db.session.get(Chamado, chamado_id)
        if not chamado:
            raise ValueError("Chamado não encontrado!")

        chamado.status = status
        db.session.commit()
        return {"mensagem": f"Status do chamado {chamado_id} atualizado para '{status}'."}

    @staticmethod
    def listar_chamados():
        """Lista todos os chamados, garantindo alias únicos para usuários"""

        Solicitante = aliased(Usuario)  # 🚀 Alias para solicitante
        Responsavel = aliased(Usuario)  # 🚀 Alias para responsável

        chamados = (
            db.session.query(
                Chamado.id, Chamado.titulo, Chamado.descricao, Setor.nome.label("setor"),
                Solicitante.nome.label("solicitante"), 
                Responsavel.nome.label("responsavel"),  # ✅ Nome correto
                Chamado.status, Chamado.prazo
            )
            .join(Setor, Chamado.setor_id == Setor.id)
            .join(Solicitante, Chamado.solicitante_id == Solicitante.id)
            .outerjoin(Responsavel, Chamado.responsavel_id == Responsavel.id)  # ✅ LEFT JOIN para responsável
            .all()
        )

        return [
            {
                "id": c.id,
                "titulo": c.titulo,
                "descricao": c.descricao,
                "setor": c.setor,
                "solicitante": c.solicitante,
                "responsavel": c.responsavel if c.responsavel else "Não atribuído",  # ✅ Evita None
                "status": c.status,
                "prazo": c.prazo
            }
            for c in chamados
        ]
        
    @staticmethod
    def buscar_por_id(chamado_id):
        """Busca um chamado específico pelo ID"""
        
        chamado = db.session.get(Chamado, chamado_id)
        if not chamado:
            raise ValueError("Chamado não encontrado!")

        return {
            "id": chamado.id,
            "titulo": chamado.titulo,
            "descricao": chamado.descricao,
            "setor": chamado.setor.nome if chamado.setor else None,
            "solicitante": chamado.solicitante.nome if chamado.solicitante else None,
            "responsavel": chamado.responsavel.nome if chamado.responsavel else None,
            "status": chamado.status,
            "prazo": chamado.prazo
        }

    @staticmethod
    def deletar_chamado(chamado_id):
        """Exclui um chamado do banco"""
        
        chamado = db.session.get(Chamado, chamado_id)
        if not chamado:
            raise ValueError("Chamado não encontrado!")

        db.session.delete(chamado)
        db.session.commit()

        return {"mensagem": f"Chamado {chamado_id} excluído com sucesso!"}
