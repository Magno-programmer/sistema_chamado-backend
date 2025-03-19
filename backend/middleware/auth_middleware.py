from functools import wraps
from flask import request, jsonify, g, current_app
import jwt

def verificar_autenticacao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Middleware para validar autenticação via JWT"""
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return jsonify({"erro": "Token de autenticação ausente ou mal formatado"}), 401

        try:
            # 🔹 Remove 'Bearer ' e valida a assinatura do token
            secret_key = current_app.config.get("SECRET_KEY", "default_secret_key")
            decoded_token = jwt.decode(
                token.split("Bearer ")[-1], secret_key, algorithms=["HS256"]
            )

            g.user_id = decoded_token.get("userId")
            g.user_role = decoded_token.get("role")  # Armazena o papel do usuário

            if not g.user_id or not g.user_role:
                return jsonify({"erro": "Token inválido: informações incompletas"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401

        return f(*args, **kwargs)

    return decorated_function
