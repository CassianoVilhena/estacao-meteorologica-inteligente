import requests
import random
import time

URL = "http://127.0.0.1:5000/dados"

while True:
    dado = {
        "temperatura": round(random.uniform(20, 35), 1),
        "umidade": round(random.uniform(40, 80), 1)
    }
    resposta = requests.post(URL, json=dado)
    print("Enviado:", dado, "->", resposta.status_code)
    time.sleep(2)