from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__, template_folder='templates')

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://...')  # já definido no Render

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

@app.route('/')
def index():
    return "Página inicial - vá para /cadastro para acessar o formulário"

if __name__ == '__main__':
    app.run(debug=True)



