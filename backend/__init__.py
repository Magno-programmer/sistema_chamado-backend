import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

# 🔹 Configurar CORS corretamente
CORS(app, resources={r"/*": {"origins": ["https://preview--chamado-facilitas.lovable.app"]}}, supports_credentials=True)

# 🔹 Conectar ao Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ssl_cert_path = os.getenv("SSL_CERT_PATH")
db_url = os.getenv("VITE_SUPABASE_DB")

# ✅ Garante que SSL é aplicado corretamente na string de conexão
if db_url and "?sslmode=" not in db_url:
    db_url += f"?sslmode=verify-ca&sslrootcert=./{ssl_cert_path}"

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db = SQLAlchemy(app)
ma = Marshmallow(app)