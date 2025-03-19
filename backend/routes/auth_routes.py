from flask import Blueprint, request, jsonify
from backend.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

# 🚀 Login do usuário
@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """Realiza a autenticação do usuário tratando diferentes tipos de entrada"""
    try:
        # 🔹 Verifica o tipo de Content-Type da requisição
        content_type = request.content_type

        if content_type == "application/json":
            data = request.get_json()
        elif content_type == "application/x-www-form-urlencoded":
            data = request.form.to_dict()  # Captura os dados de um formulário
        elif content_type == "multipart/form-data":
            data = {key: request.form[key] for key in request.form}  # Formulário com arquivos
        elif content_type == "text/plain":
            data = {"raw_text": request.data.decode("utf-8")}  # Lê o texto puro
        else:
            return jsonify({"erro": f"Tipo de requisição '{content_type}' não suportado"}), 415

        if not data:
            return jsonify({"erro": "Nenhum dado recebido"}), 400

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
