from flask import Blueprint, jsonify, request, g
from backend.services.setor_service import SetorService
from backend.middleware.auth_middleware import verificar_autenticacao

setores_bp = Blueprint("setores", __name__)

# 🔹 Função para validar se usuário tem permissão de ADMIN
def verificar_admin():
    if g.user_role not in ["ADMIN"]:
        return jsonify({"erro": "Apenas administradores podem executar esta ação"}), 403

@setores_bp.route("/setores", methods=["GET"])
@verificar_autenticacao
def listar_setores():
    """Lista todos os setores disponíveis"""
    try:
        setores = SetorService.listar_setores()
        return jsonify(setores), 200  # 🚀 Converte cada Setor para dicionário
    except Exception as e:
        return jsonify({"erro": "Erro ao listar setores", "message": str(e)}), 500

@setores_bp.route("/setores", methods=["POST"])
@verificar_autenticacao
def criar_setor():
    """Cria um novo setor no sistema (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        data = request.get_json()
        nome = data.get("nome")

        if not nome:
            return jsonify({"erro": "O nome do setor é obrigatório"}), 400

        setor_id = SetorService.criar_setor(nome)
        return jsonify({"mensagem": "Setor criado com sucesso!", "id": setor_id}), 201

    except Exception as e:
        return jsonify({"erro": "Erro ao criar setor", "message": str(e)}), 500

@setores_bp.route("/setores/<int:setor_id>", methods=["DELETE"])
@verificar_autenticacao
def deletar_setor(setor_id):
    """Exclui um setor do sistema (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        setor = SetorService.buscar_por_id(setor_id)
        if not setor:
            return jsonify({"erro": "Setor não encontrado!"}), 404  # 🔥 Garante que o setor existe

        # 🚀 Verifica se existem usuários ou chamados vinculados ao setor
        if SetorService.setor_tem_usuarios(setor_id):
            return jsonify({"erro": "Não é possível excluir o setor, pois existem usuários vinculados"}), 400

        if SetorService.setor_tem_chamados(setor_id):
            return jsonify({"erro": "Não é possível excluir o setor, pois existem chamados vinculados"}), 400

        SetorService.deletar_setor(setor_id)
        return jsonify({"mensagem": "Setor excluído com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao excluir setor", "message": str(e)}), 500
