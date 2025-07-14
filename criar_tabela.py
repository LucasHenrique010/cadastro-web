import psycopg2

# Sua URL externa do banco na Render
DATABASE_URL = 'postgresql://cadastro_user_w50s_user:vsbsuj4sTIAVwbfouVeTQrbS6rS1ibmF@dpg-d1q6rcjuibrs73edb0c0-a.oregon-postgres.render.com/cadastro_user_w50s'

# SQL para criar a tabela
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
    # Conecta ao banco
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Cria a tabela
    cur.execute(SQL_CREATE_TABELA)
    conn.commit()

    print("✅ Tabela 'cadastro_responsaveis' criada (ou já existia).")

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Erro ao conectar ou criar a tabela:", e)
