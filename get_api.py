import requests
import time

# Defina o número de vezes que você quer chamar a API
num_requests = 10

# URL da API de conselhos e do seu endpoint local
advice_url = "https://api.adviceslip.com/advice"
local_endpoint = "http://localhost:5001/data"

# Função para obter conselhos da API
def get_advice():
    response = requests.get(advice_url)
    if response.status_code == 200:
        data = response.json()
        return data['slip']['advice']  # Acessa o conselho
    else:
        return None

# Função para enviar os dados para o seu endpoint
def send_data(data):
    payload = {
        "date": int(time.time()),  # Data em formato UNIX timestamp
        "dados": data
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(local_endpoint, json=payload, headers=headers)
    return response.status_code

# Executa o loop para realizar as chamadas e enviar os dados
for i in range(num_requests):
    advice = get_advice()
    print(advice)
    if advice:
        status = send_data(advice)
        print(f"Conselho enviado: {advice} - Status: {status}")
    else:
        print("Erro ao obter conselho.")
    time.sleep(1)  # Aguarda 1 segundo entre as chamadas
