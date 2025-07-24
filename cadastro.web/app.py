from flask import Flask, render_template, request
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não está definida no .env")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            dia_vencimento = int(request.form['data_vencimento'])
            hoje = datetime.today()
            data_vencimento = datetime(hoje.year, hoje.month, dia_vencimento).date()

            dados = (
                request.form['nome_responsavel'],
                request.form['cpf_responsavel'],
                request.form['telefone'],
                request.form['nome_crianca'],
                request.form['endereco'],
                request.form['escola'],
                0.0,  # valor fixo
                data_vencimento
            )

            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO cadastro_responsaveis
                (nome_responsavel, cpf, telefone, nome_crianca, endereco, escola, valor, data_vencimento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, dados)
            conn.commit()
            cur.close()
            conn.close()

            return render_template('cadastro.html', sucesso=True)

        except Exception as e:
            return f"Erro ao salvar no banco: {e}"

    return render_template('cadastro.html', sucesso=False)

if __name__ == '__main__':
    app.run(debug=True)
