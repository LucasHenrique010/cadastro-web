from flask import Flask, render_template, request
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

app = Flask(__name__)

# URL do banco remoto (Render)
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://database_url_be4c_user:BCRx7VZlKPOMOlBWwYmdKhMjK2fq9UAL@dpg-d0jms4odl3ps73cm4s9g-a.oregon-postgres.render.com/database_url_be4c'
)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            # Pega o dia do vencimento do formulário
            dia_vencimento = int(request.form['data_vencimento'])
            hoje = datetime.today()
            data_vencimento = datetime(hoje.year, hoje.month, dia_vencimento).date()

            # Coleta os dados do formulário
            dados = (
                request.form['nome_responsavel'],
                request.form['cpf_responsavel'],
                request.form['telefone'],
                request.form['nome_crianca'],
                request.form['endereco'],
                request.form['escola'],
                0.0,  # Valor fixo (pode ser alterado no futuro)
                data_vencimento
            )

            # Conecta ao banco e insere os dados
            conn = psycopg2.connect(DATABASE_URL)
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
