from flask import Blueprint, jsonify, request, g
from backend.services.chamado_service import ChamadoService
from backend.middleware.auth_middleware import verificar_autenticacao

chamados_bp = Blueprint("chamados", __name__)

# 🔹 Função para validar se usuário tem permissão de ADMIN
def verificar_admin():
    if g.user_role not in ["ADMIN"]:
        return jsonify({"erro": "Apenas administradores podem executar esta ação"}), 403

# 🚀 Criar um chamado
@chamados_bp.route("/chamados", methods=["POST"])
@verificar_autenticacao
def criar_chamado():
    """Cria um novo chamado vinculado ao usuário logado"""
    try:
        data = request.get_json()
        titulo = data.get("titulo")
        descricao = data.get("descricao")
        setor_id = data.get("setor_id")
        prazo = data.get("prazo")

        if not all([titulo, descricao, setor_id, prazo]):
            return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

        chamado_id = ChamadoService.criar_chamado(titulo, descricao, g.user_id, setor_id, prazo)
        return jsonify({"mensagem": "Chamado criado com sucesso!", "id": chamado_id}), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except Exception as e:
        return jsonify({"erro": "Erro ao criar chamado", "message": str(e)}), 500

# 🚀 Listar todos os chamados
@chamados_bp.route("/chamados", methods=["GET"])
@verificar_autenticacao
def listar_chamados():
    """Lista todos os chamados"""
    try:
        chamados = ChamadoService.listar_chamados()
        return jsonify(chamados), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao listar chamados", "message": str(e)}), 500

# 🚀 Atualizar status de um chamado
@chamados_bp.route("/chamados/<int:chamado_id>", methods=["PUT"])
@verificar_autenticacao
def atualizar_chamado(chamado_id):
    """Atualiza o status de um chamado"""
    try:
        data = request.get_json()
        status = data.get("status")

        if status not in ["Aberto", "Em Andamento", "Concluído", "Atrasado"]:
            return jsonify({"erro": "Status inválido"}), 400

        ChamadoService.atualizar_status(chamado_id, status)
        return jsonify({"mensagem": "Chamado atualizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar chamado", "message": str(e)}), 500

# 🚀 Buscar um chamado por ID
@chamados_bp.route("/chamados/<int:chamado_id>", methods=["GET"])
@verificar_autenticacao
def buscar_chamado_por_id(chamado_id):
    """Busca um chamado pelo ID"""
    try:
        chamado = ChamadoService.buscar_por_id(chamado_id)
        if chamado:
            return jsonify(chamado), 200
        return jsonify({"erro": "Chamado não encontrado!"}), 404
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar chamado", "message": str(e)}), 500

# 🚀 Deletar um chamado
@chamados_bp.route("/chamados/<int:chamado_id>", methods=["DELETE"])
@verificar_autenticacao
def deletar_chamado(chamado_id):
    """Exclui um chamado (somente Admins ou dono do chamado)"""
    try:
        chamado = ChamadoService.buscar_por_id(chamado_id)

        if not chamado:
            return jsonify({"erro": "Chamado não encontrado"}), 404

        # 🚀 O usuário pode excluir apenas seus próprios chamados, Admins podem excluir qualquer chamado
        if chamado["solicitante"] != g.user_id and g.user_role not in ["ADMIN"]:
            return jsonify({"erro": "Você não tem permissão para excluir este chamado"}), 403

        ChamadoService.deletar_chamado(chamado_id)
        return jsonify({"mensagem": "Chamado excluído com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao excluir chamado", "message": str(e)}), 500
