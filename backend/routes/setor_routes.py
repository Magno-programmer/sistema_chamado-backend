from flask import Blueprint, jsonify, request, g
from backend.services.setor_service import SetorService
from backend.middleware.auth_middleware import verificar_autenticacao

setores_bp = Blueprint("setores", __name__)

# 🔹 Função para validar se usuário tem permissão de ADMIN
def verificar_admin():
    if g.user_role not in ["ADMIN"]:
        return jsonify({"erro": "Apenas administradores podem executar esta ação"}), 403

# 🚀 Listar todos os setores
@setores_bp.route("/setores", methods=["GET"])
@verificar_autenticacao
def listar_setores():
    """Lista todos os setores disponíveis"""
    try:
        setores = SetorService.listar_setores()
        return jsonify(setores), 200  # 🚀 Retorna corretamente agora
    except Exception as e:
        return jsonify({"erro": "Erro ao listar setores", "message": str(e)}), 500

# 🚀 Criar um novo setor
@setores_bp.route("/setores", methods=["POST"])
@verificar_autenticacao
def criar_setor():
    """Cria um novo setor no sistema (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        content_type = request.content_type
        data = None

        # 🔹 Suporte a diferentes tipos de Content-Type
        if content_type == "application/json":
            data = request.get_json()
        elif content_type == "application/x-www-form-urlencoded":
            data = request.form.to_dict()
        elif content_type == "multipart/form-data":
            data = {key: request.form[key] for key in request.form}
        elif content_type == "text/plain":
            data = {"raw_text": request.data.decode("utf-8")}
        else:
            return jsonify({"erro": f"Tipo de requisição '{content_type}' não suportado"}), 415

        if not data:
            return jsonify({"erro": "Nenhum dado recebido"}), 400

        nome = data.get("nome")

        if not nome:
            return jsonify({"erro": "O nome do setor é obrigatório"}), 400

        setor_id = SetorService.criar_setor(nome)
        return jsonify({"mensagem": "Setor criado com sucesso!", "id": setor_id}), 201

    except Exception as e:
        return jsonify({"erro": "Erro ao criar setor", "message": str(e)}), 500

# 🚀 Atualizar um setor por ID
@setores_bp.route("/setores/<int:setor_id>", methods=["PUT"])
@verificar_autenticacao
def atualizar_setor(setor_id):
    """Atualiza os detalhes de um setor (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        data = request.get_json()
        novo_nome = data.get("nome")

        if not novo_nome:
            return jsonify({"erro": "O nome do setor é obrigatório para atualização"}), 400

        resultado, status_code = SetorService.atualizar_setor(setor_id, novo_nome)
        return jsonify(resultado), status_code  # Retorna mensagem e código HTTP

    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar setor", "message": str(e)}), 500

# 🚀 Buscar um setor por ID
@setores_bp.route("/setores/<int:setor_id>", methods=["GET"])
@verificar_autenticacao
def buscar_setor_por_id(setor_id):
    """Retorna um setor específico pelo ID"""
    try:
        setor = SetorService.buscar_por_id(setor_id)
        if setor:
            return jsonify(setor), 200
        return jsonify({"erro": "Setor não encontrado!"}), 404
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar setor", "message": str(e)}), 500

# 🚀 Deletar um setor por ID
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
