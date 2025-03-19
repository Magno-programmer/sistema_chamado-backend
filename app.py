from backend import app
from backend.routes.chamados_routes import chamados_bp
from backend.routes.auth_routes import auth_bp
from backend.routes.setor_routes import setores_bp  # 🚀 Novo import
from backend.routes.usuario_routes import usuarios_bp  # 🚀 Novo import
from backend.routes.prazo_routes import prazos_bp  # 🚀 Novo import

# Registrar as rotas
app.register_blueprint(chamados_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(setores_bp)  # Adicionar as rotas de setores
app.register_blueprint(usuarios_bp)  # 🚀 Adicionar as rotas de usuários
app.register_blueprint(prazos_bp)  # 🚀 Adicionar as rotas de prazos

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
