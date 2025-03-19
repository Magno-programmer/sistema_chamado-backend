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
CORS(app, resources={r"/*": {"origins": ["https://chamado-facilitas.lovable.app/"]}}, supports_credentials=True)

# 🔹 Conectar ao Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

db_url = os.getenv("VITE_SUPABASE_DB")

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Define o caminho onde o certificado será salvo temporariamente
ssl_cert_path = "/supabase.crt"
supabase_cert_content = os.getenv("SUPABASE_CERT")

# Obtém o certificado da variável de ambiente e escreve no arquivo
if supabase_cert_content:
    with open(ssl_cert_path, "w") as cert_file:
        cert_file.write(supabase_cert_content)

# Atualiza a URL do banco para usar o certificado SSL gerado
if db_url and "?sslmode=" not in db_url:
    db_url += f"?sslmode=verify-ca&sslrootcert={ssl_cert_path}"
    
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db = SQLAlchemy(app)
ma = Marshmallow(app)