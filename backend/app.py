import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir acesso do frontend

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/clima')
def clima():
    cidade = request.args.get('cidade')
    if not cidade:
        return jsonify({"erro": "Informe uma cidade"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"

    try:
        resposta = requests.get(url)
        dados = resposta.json()

        if resposta.status_code != 200:
            return jsonify({"erro": dados.get("message", "Erro desconhecido")}), resposta.status_code

        clima_info = {
            "cidade": dados["name"],
            "temperatura": dados["main"]["temp"],
            "sensacao_termica": dados["main"]["feels_like"],
            "descricao": dados["weather"][0]["description"],
            "icone": dados["weather"][0]["icon"]
        }

        return jsonify(clima_info)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
