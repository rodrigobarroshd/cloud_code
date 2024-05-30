import requests
import random
import string
import json

# Função para gerar um nome aleatório
def generate_random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

# Função para gerar um valor aleatório
def generate_random_value():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))

# Número de JSON que você deseja enviar
num_json = 80

# URL para onde você enviará os JSON via POST
url = 'http://localhost:5000/'

# Enviar os JSON via POST
for i in range(num_json):
    # Gerar um par de chave-valor aleatório
    key = f"name{random.randint(100, 999)}"
    value = generate_random_value()

    # Construir o JSON com o par de chave-valor aleatório
    data = {key: value}

    # Enviar a solicitação HTTP POST com o JSON
    response = requests.post(url, json=data)

    # Verificar se a solicitação foi bem-sucedida
    if response.status_code == 200:
        print(f"JSON enviado com sucesso: {data}")
    else:
        print(f"Falha ao enviar JSON: {data}, Status code: {response.status_code}")
