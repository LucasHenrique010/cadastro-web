import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não está definida no .env")

SQL_CREATE_TABELA = """
CREATE TABLE IF NOT EXISTS cadastro_responsaveis (
    id SERIAL PRIMARY KEY,
    nome_responsavel VARCHAR(100),
    cpf VARCHAR(14),
    telefone VARCHAR(20),
    nome_crianca VARCHAR(100),
    endereco TEXT,
    escola VARCHAR(100),
    valor NUMERIC(10, 2),
    data_vencimento DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute(SQL_CREATE_TABELA)
    conn.commit()

    print("✅ Tabela 'cadastro_responsaveis' criada (ou já existia).")

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Erro ao conectar ou criar a tabela:", e)

