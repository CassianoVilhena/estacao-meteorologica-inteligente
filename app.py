
import sqlite3
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
import random

app = Flask(__name__)

PASTA = Path(__file__).resolve().parent
BANCO = PASTA / "estacao.db"

ESTACAO = {
    "nome": "Estação meteorológica - Santana de Parnaíba",
    "latitude": -23.4439,
    "longitude": -46.9183
}

def conectar():
    return sqlite3.connect(BANCO)

def criar_tabela():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leituras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperatura REAL,
                umidade REAL,
                horario TEXT
            )
        """)

@app.route("/")
def dashboard():
    return send_file(PASTA / "dashboard.html")

@app.route("/estacao")
def estacao():
    return jsonify(ESTACAO)

@app.route("/dados", methods=["POST"])
def receber_dados():
    dado = request.get_json(silent=True)

    if not dado or "temperatura" not in dado or "umidade" not in dado:
        return jsonify({"erro": "Dados inválidos"}), 400

    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with conectar() as conn:
        conn.execute(
            """INSERT INTO leituras
            (temperatura, umidade, horario)
            VALUES (?, ?, ?)""",
            (dado["temperatura"], dado["umidade"], horario)
        )

    print("Recebido:", dado)
    return jsonify({"status": "ok"})


def gerar_leitura_simulada():
    temperatura = round(random.uniform(20, 35), 1)
    umidade = round(random.uniform(40, 80), 1)
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with conectar() as conn:
        conn.execute(
            """INSERT INTO leituras
            (temperatura, umidade, horario)
            VALUES (?, ?, ?)""",
            (temperatura, umidade, horario)
        )


@app.route("/dados", methods=["GET"])
def listar_dados():
    gerar_leitura_simulada()

    with conectar() as conn:
        linhas = conn.execute(
            """SELECT temperatura, umidade, horario
            FROM leituras ORDER BY id DESC LIMIT 50"""
        ).fetchall()

    resultado = [
        {"temperatura": t, "umidade": u, "horario": h}
        for t, u, h in linhas
    ]

    return jsonify(resultado)

criar_tabela()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
