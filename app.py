from flask import Flask, request
import json
import paho.mqtt.client as mqtt

# Configurações do MQTT
broker_address = "jackal.rmq.cloudamqp.com"
port = 1883
topic = "meu_topico"
username = 'xyoowllx:xyoowllx'
password = 'Gle6D-nfdPPGDfg-uLDfQLw9W349orBv'

# Cria o aplicativo Flask
app = Flask(__name__)

# Cria o cliente MQTT
client = mqtt.Client()

# Define a função de callback para conexão
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
    else:
        print(f"Falha ao conectar, código de erro: {rc}")

# Define a função de callback para publicação
def on_publish(client, userdata, mid):
    print("Mensagem publicada!")

# Define o callback para conexão
client.on_connect = on_connect
# Define o callback para publicação
client.on_publish = on_publish

# Configura as credenciais do MQTT
client.username_pw_set(username, password)

# Conecta ao broker MQTT
client.connect(broker_address, port, keepalive=60)

# Inicia o loop do cliente MQTT em segundo plano
client.loop_start()

# Define a rota para receber o POST
@app.route("/", methods=["POST"])
def receive_message():
    # Recebe a mensagem JSON do corpo da requisição
    message_json = request.get_json()

    # Processa a mensagem JSON
    process_message(message_json)

    # Retorna uma resposta JSON simples
    return json.dumps({"mensagem": "Mensagem recebida e publicada com sucesso!"})

# Função para processar a mensagem JSON e publicar no MQTT
def process_message(message_json):
    try:
        # Verifica se a mensagem JSON é um dicionário
        if isinstance(message_json, dict):
            # Extrai o tópico e a mensagem do dicionário
            topic = list(message_json.keys())[0]
            message = message_json[topic]

            # Publica a mensagem no MQTT
            publish_message(topic, message)
        else:
            raise TypeError("Mensagem JSON deve ser um dicionário.")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Função para publicar a mensagem no MQTT
def publish_message(topic, message):
    client.publish(topic, message)

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
