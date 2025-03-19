import datetime
import jwt
from backend.services.auth_service import AuthService
from flask import jsonify, make_response, current_app

class AuthController:
    @staticmethod
    def login(email, password):
        user_data = AuthService.authenticate(email, password)
        print(user_data)
    
        if not user_data:
            return jsonify({"erro": "Credenciais inválidas"}), 401
        # ✅ Gera o token JWT corretamente
        token_payload = {
            "userId": user_data["userId"],
            "email": user_data["email"],
            "role": user_data["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Expira em 30 minutos
        }
        access_token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm="HS256")

        # ✅ Criar resposta e definir cookie seguro
        response = make_response(jsonify({"User_id": user_data["userId"], "access_token": access_token}))

        return response

    @staticmethod
    def logout():
        return jsonify({"mensagem": "Logout realizado com sucesso!"}), 200
