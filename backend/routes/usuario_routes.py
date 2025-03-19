import uuid
from flask import Blueprint, jsonify, request, g
from backend.services.usuario_service import UsuarioService
from backend.middleware.auth_middleware import verificar_autenticacao

usuarios_bp = Blueprint("usuarios", __name__)

# 🔹 Função para validar se usuário tem permissão de ADMIN
def verificar_admin():
    if g.user_role not in ["ADMIN"]:
        return jsonify({"erro": "Apenas administradores podem executar esta ação"}), 403

@usuarios_bp.route("/usuarios", methods=["POST"])
@verificar_autenticacao
def criar_usuario():
    """Cria um novo usuário no sistema (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        data = request.get_json()
        id = uuid.uuid4().hex
        nome = data.get("nome")
        email = data.get("email")
        setor_id = data.get("setor_id")
        role = data.get("role")
        senha = data.get("senha")

        if not all([nome, email, setor_id, role, senha]):
            return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

        usuario_id = UsuarioService.criar_usuario(id, nome, email, setor_id, role, senha)
        return jsonify({"mensagem": "Usuário criado com sucesso!", "id": usuario_id}), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao criar usuário", "message": str(e)}), 500

@usuarios_bp.route("/usuarios/<string:user_id>", methods=["DELETE"])
@verificar_autenticacao
def deletar_usuario(user_id):
    """Exclui um usuário do sistema (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        usuario = UsuarioService.buscar_por_id(user_id)

        if not usuario:
            return jsonify({"mensagem": "Usuário não encontrado"}), 404

        if usuario.id == g.user_id:
            return jsonify({"erro": "Você não pode excluir sua própria conta"}), 403  # 🔥 Protege admin de se excluir

        if UsuarioService.usuario_tem_chamados_abertos(usuario):
            return jsonify({"erro": "Não é possível excluir o usuário, pois ele possui chamados em aberto"}), 400

        UsuarioService.deletar_usuario(user_id)
        return jsonify({"mensagem": "Usuário excluído com sucesso!"}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao excluir usuário", "message": str(e)}), 500

@usuarios_bp.route("/usuarios", methods=["GET"])
@verificar_autenticacao
def listar_usuarios():
    """Lista todos os usuários (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        usuarios = UsuarioService.listar_usuarios()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar usuários", "message": str(e)}), 500

@usuarios_bp.route("/usuarios/email", methods=["GET"])
@verificar_autenticacao
def buscar_usuario_por_email():
    """Busca um usuário pelo e-mail (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        email = request.args.get("email")
        if not email:
            return jsonify({"erro": "E-mail é obrigatório"}), 400

        usuario = UsuarioService.buscar_por_email(email)
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar usuário", "message": str(e)}), 500

@usuarios_bp.route("/usuarios/<string:user_id>", methods=["PUT"])
@verificar_autenticacao
def atualizar_usuario(user_id):
    """Atualiza um usuário no sistema (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        data = request.get_json()
        nome = data.get("nome")
        email = data.get("email")
        setor_id = data.get("setor_id")

        if not any([nome, email, setor_id]):
            return jsonify({"erro": "Pelo menos um campo (nome, email ou setor) deve ser informado"}), 400

        usuario_atualizado = UsuarioService.atualizar_usuario(user_id, nome, email, setor_id)

        if usuario_atualizado is None:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        if not usuario_atualizado:
            return jsonify({"mensagem": "Nenhuma alteração realizada"}), 200  # 🔹 Se não houver mudanças

        return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar usuário", "message": str(e)}), 500
