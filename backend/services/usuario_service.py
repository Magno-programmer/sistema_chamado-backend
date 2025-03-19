from backend import db
from backend.models.usuario_model import Usuario
from flask import g
from sqlalchemy.exc import IntegrityError
import uuid

class UsuarioService:

    @staticmethod
    def listar_usuarios():
        """Lista todos os usuários e retorna os detalhes com o nome do setor"""
        from backend.models.setor_model import Setor  # Importação dentro da função para evitar circular import
        
        usuarios = db.session.query(
            Usuario.id, Usuario.nome, Usuario.email, Setor.nome.label("setor"), Usuario.role, Usuario.senha_hash
        ).join(Setor, Usuario.setor_id == Setor.id).all()

            # 🔹 Converte os resultados (tuplas) para dicionários
        return [
            {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "setor": usuario.setor,
                "role": usuario.role
            }
            for usuario in usuarios
        ]

    @staticmethod
    def criar_usuario(id, nome, email, setor_id, role, senha):
        """Cria um novo usuário no banco de dados"""
        from backend.models.setor_model import Setor  # Importação dentro da função para evitar circular import

        # 🔹 Verificar se o setor existe
        setor = db.session.get(Setor, setor_id)
        if not setor:
            raise ValueError("Setor inválido! O ID do setor não existe.")

        senha_hash = Usuario.hashing_pwd(senha)

        novo_usuario = Usuario(
            id=id,
            nome=nome,
            email=email,
            setor_id=setor_id,
            role=role,
            senha_hash=senha_hash
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return novo_usuario.id
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erro ao criar usuário. Verifique se o e-mail já está cadastrado.")

    @staticmethod
    def usuario_tem_chamados_abertos(usuario_id):
        """Verifica se o usuário possui chamados em aberto antes de ser excluído"""
        from backend.models.chamado_model import Chamado  # Evita circular import
        
        chamados_abertos = db.session.query(Chamado).filter(
            Chamado.solicitante_id == usuario_id,
            Chamado.status.in_(["Aberto", "Em Andamento"])
        ).count()

        return chamados_abertos > 0  # Retorna True se houver chamados em aberto

    @staticmethod
    def deletar_usuario(user_id):
        """Exclui um usuário do banco se não tiver chamados em aberto"""
        usuario = db.session.get(Usuario, user_id)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if UsuarioService.usuario_tem_chamados_abertos(user_id):
            raise ValueError("Usuário possui chamados em aberto e não pode ser excluído.")

        db.session.delete(usuario)
        db.session.commit()

    @staticmethod
    def buscar_por_email(email):
        """Busca um usuário pelo e-mail"""
        usuario = Usuario.query.filter_by(email=email).first()
        return usuario

    @staticmethod
    def atualizar_usuario(user_id, nome=None, email=None, setor_id=None):
        """Atualiza um usuário no banco"""
        usuario = db.session.get(Usuario, user_id)
        if not usuario:
            return None  # Usuário não encontrado

        if nome:
            usuario.nome = nome
        if email:
            usuario.email = email
        if setor_id:
            from backend.models.setor_model import Setor
            setor = db.session.get(Setor, setor_id)
            if not setor:
                raise ValueError("Setor inválido! O ID do setor não existe.")
            usuario.setor_id = setor_id

        db.session.commit()
        return True  # Usuário atualizado com sucesso
