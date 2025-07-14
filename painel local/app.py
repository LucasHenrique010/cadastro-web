from flask import Flask, render_template, request, redirect, url_for, session, send_file
import psycopg2
import pandas as pd
import os
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Altere isso para algo seguro

# URL do banco de dados remoto
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://usuario:senha@host:porta/nome_do_banco')

# Credenciais simples para login
USUARIO = 'admin'
SENHA = '1234'

def conectar_db():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == USUARIO and request.form['senha'] == SENHA:
            session['logado'] = True
            return redirect(url_for('listar'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos')
    return render_template('login.html')

@app.route('/listar')
def listar():
    if not session.get('logado'):
        return redirect(url_for('login'))

    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registros")
    registros = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('listar.html', registros=registros)

@app.route('/exportar')
def exportar():
    if not session.get('logado'):
        return redirect(url_for('login'))

    conn = conectar_db()
    df = pd.read_sql("SELECT * FROM registros", conn)
    conn.close()

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Registros')
        writer.save()
    output.seek(0)

    return send_file(output, download_name='registros.xlsx', as_attachment=True)

@app.route('/limpar')
def limpar():
    if not session.get('logado'):
        return redirect(url_for('login'))

    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM registros")
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('listar'))

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
