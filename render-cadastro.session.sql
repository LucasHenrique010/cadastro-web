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
