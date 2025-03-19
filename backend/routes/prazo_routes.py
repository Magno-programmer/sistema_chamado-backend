from flask import Blueprint, jsonify, request, render_template, g
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
        return jsonify(prazos) # ✅ Retorna corretamente agora
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
        data = request.get_json()
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
