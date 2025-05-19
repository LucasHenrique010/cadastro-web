from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# URL do banco remoto (externa)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://database_url_be4c_user:BCRx7VZlKPOMOlBWwYmdKhMjK2fq9UAL@dpg-d0jms4odl3ps73cm4s9g-a.oregon-postgres.render.com/database_url_be4c')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        dados = (
            request.form['nome_responsavel'],
            request.form['cpf_responsavel'],
            request.form['telefone'],
            request.form['email'],
            request.form['endereco'],
            request.form['nome_crianca'],
            request.form['escola'],
            request.form['data_vencimento']
        )

        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO registros 
                (nome_responsavel, cpf_responsavel, telefone, email, endereco, nome_crianca, escola, data_vencimento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, dados)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            return f"Erro ao salvar no banco: {e}"

        return render_template('cadastro.html', sucesso=True)

    return render_template('cadastro.html', sucesso=False)

if __name__ == '__main__':
    app.run(debug=True)
