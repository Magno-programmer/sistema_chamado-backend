import os
from flask import jsonify, make_response
from backend import db
from backend.models.usuario_model import Usuario
from backend.services.usuario_service import UsuarioService
from werkzeug.security import check_password_hash
from supabase import create_client, Client
import jwt
import datetime

# 🔹 Configuração do Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Configuração do JWT
SECRET_KEY = os.getenv("SECRET_KEY")  # 🔥 Troque por um valor seguro em produção!

class AuthService:

    @staticmethod
    def authenticate(email, password):
        """Autentica um usuário, verificando senha e retornando JWT"""
        
        user = UsuarioService.buscar_por_email(email=email)
        
        if not user: 
            return make_response(jsonify({"erro": "Usuário não encontrado"}), 400)
        
        if not check_password_hash(user.senha_hash, password):  # 🔹 Usa hashing seguro
            return make_response(jsonify({"erro": "Senha incorreta"}), 403)
        
        # 🔥 Gera token JWT com tempo de expiração
        token = AuthService.generate_token(user)

        return {
            "userId": user.id,
            "email": email,
            "role": user.role.upper(),
            "token": token
        }

    @staticmethod
    def generate_token(user):
        """Gera um token JWT válido por 24 horas"""
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 🔥 Expira em 24h
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_token(token):
        """Verifica se o token JWT é válido"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return {"erro": "Token expirado"}, 401
        except jwt.InvalidTokenError:
            return {"erro": "Token inválido"}, 401
