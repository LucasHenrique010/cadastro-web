from flask import Flask, render_template, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# URL do banco remoto (externa)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://database_url_be4c_user:BCRx7VZlKPOMOlBWwYmdKhMjK2fq9UAL@dpg-d0jms4odl3ps73cm4s9g-a.oregon-postgres.render.com/database_url_be4c')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            # Pega o dia do vencimento do formulário e monta uma data completa
            dia_vencimento = int(request.form['data_vencimento'])
            hoje = datetime.today()
            # Monta a data com o ano e mês atual e o dia do vencimento
            data_vencimento = datetime(hoje.year, hoje.month, dia_vencimento).date()

            dados = (
                request.form['nome_responsavel'],
                request.form['cpf_responsavel'],  # no banco é cpf
                request.form['telefone'],
                request.form['nome_crianca'],
                request.form['endereco'],
                request.form['escola'],
                0.0,  # valor fixo, você pode adicionar no form depois se quiser
                data_vencimento
            )

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
        except Exception as e:
            return f"Erro ao salvar no banco: {e}"

        return render_template('cadastro.html', sucesso=True)

    return render_template('cadastro.html', sucesso=False)







