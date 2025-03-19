from flask import Blueprint, request, jsonify
from backend.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

# 🚀 Login do usuário
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """Realiza a autenticação do usuário"""
    try:
        
        if request.content_type != "application/json":
            return jsonify({"erro": "Content-Type deve ser application/json"}), 415  # ✅ Retorna erro se não for JSON
        
        data = request.get_json()

        if not data:
            return jsonify({"erro": "Requisição inválida, JSON esperado"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

        return AuthController.login(email, password)

    except Exception as e:
        return jsonify({"erro": "Erro ao processar login", "message": str(e)}), 500

# 🚀 Logout do usuário
@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    """Realiza o logout do usuário"""
    try:
        return AuthController.logout()
    except Exception as e:
        return jsonify({"erro": "Erro ao processar logout", "message": str(e)}), 500
