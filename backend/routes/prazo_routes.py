from flask import Blueprint, jsonify, request, g
from backend.services.prazo_service import PrazoService
from backend.middleware.auth_middleware import verificar_autenticacao

prazos_bp = Blueprint("prazos", __name__)

# 🔹 Função para validar se usuário tem permissão de ADMIN
def verificar_admin():
    if g.user_role not in ["ADMIN"]:
        return jsonify({"erro": "Apenas administradores podem executar esta ação"}), 403

# 🚀 Listar todos os prazos
@prazos_bp.route("/prazos", methods=["GET"])
@verificar_autenticacao
def listar_prazos():
    """Retorna todos os prazos disponíveis"""
    try:
        prazos = PrazoService.listar_prazos()
        return jsonify(prazos)  # ✅ Retorna corretamente agora
    except Exception as e:
        return jsonify({"erro": "Erro ao listar prazos", "message": str(e)}), 500

# 🚀 Criar um novo prazo
@prazos_bp.route("/prazos", methods=["POST"])
@verificar_autenticacao
def criar_prazo():
    """Cria um novo prazo (Apenas ADMIN)"""
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

        titulo = data.get("titulo")
        setor_id = data.get("setor_id")
        prazo = data.get("prazo")

        if not titulo or not setor_id or not prazo:
            return jsonify({"erro": "Todos os campos (título, setor e prazo) são obrigatórios!"}), 400

        novo_prazo = PrazoService.criar_prazo(titulo, setor_id, prazo)
        return jsonify(novo_prazo), 201  # Retorna ID e mensagem de sucesso

    except Exception as e:
        return jsonify({"erro": "Erro ao criar prazo", "message": str(e)}), 500

# 🚀 Buscar um prazo específico por ID
@prazos_bp.route("/prazos/<int:prazo_id>", methods=["GET"])
@verificar_autenticacao
def buscar_prazo_por_id(prazo_id):
    """Retorna um prazo específico pelo ID"""
    try:
        prazo = PrazoService.buscar_prazo_por_id(prazo_id)
        if prazo:
            return jsonify(prazo), 200
        return jsonify({"erro": "Prazo não encontrado!"}), 404
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar prazo", "message": str(e)}), 500

# 🚀 Atualizar um prazo por ID
@prazos_bp.route("/prazos/<int:prazo_id>", methods=["PUT"])
@verificar_autenticacao
def atualizar_prazo(prazo_id):
    """Atualiza os detalhes de um prazo (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        data = request.get_json()
        novo_titulo = data.get("titulo")
        novo_prazo = data.get("prazo")

        if not novo_titulo and not novo_prazo:
            return jsonify({"erro": "Pelo menos um campo deve ser atualizado"}), 400

        resultado, status_code = PrazoService.atualizar_prazo(prazo_id, novo_titulo, novo_prazo)
        return jsonify(resultado), status_code  # Retorna mensagem e código HTTP

    except Exception as e:
        return jsonify({"erro": "Erro ao atualizar prazo", "message": str(e)}), 500

# 🚀 Deletar um prazo específico por ID
@prazos_bp.route("/prazos/<int:prazo_id>", methods=["DELETE"])
@verificar_autenticacao
def deletar_prazo_por_id(prazo_id):
    """Exclui um prazo pelo ID (Apenas ADMIN)"""
    if (erro := verificar_admin()):
        return erro

    try:
        prazo = PrazoService.buscar_prazo_por_id(prazo_id)
        if not prazo:
            return jsonify({"erro": "Prazo não encontrado!"}), 404

        resultado, status_code = PrazoService.deletar_prazo_por_id(prazo_id)
        return jsonify(resultado), status_code  # Retorna mensagem e código HTTP

    except Exception as e:
        return jsonify({"erro": "Erro ao excluir prazo", "message": str(e)}), 500
