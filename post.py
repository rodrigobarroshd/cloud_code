import requests
import random
import string

# URL para onde você enviará os JSON via POST
url = 'http://localhost:5000/'

# Número de JSON que você deseja enviar
num_json = 20


def generate_random_value():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))


# Enviar os JSON via POST
for i in range(1, num_json+1):
    # Construir o JSON com o nome sequencial e um valor aleatório
    key = f"name{i}"
    value = generate_random_value()  # você pode substituir por um valor aleatório se desejar
    data = {key: value}

    # Enviar a solicitação HTTP POST com o JSON
    response = requests.post(url, json=data)

    # Verificar se a solicitação foi bem-sucedida
    if response.status_code == 200:
        print(f"JSON enviado com sucesso: {data}")
    else:
        print(f"Falha ao enviar JSON: {data}, Status code: {response.status_code}")
