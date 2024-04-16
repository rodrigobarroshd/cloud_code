from flask import Flask, request
import json
import paho.mqtt.client as mqtt

# Configurações do MQTT
broker_address = "jackal.rmq.cloudamqp.com"
port = 1883
# topic = "meu_topico"
username = 'xyoowllx:xyoowllx'
password = 'Gle6D-nfdPPGDfg-uLDfQLw9W349orBv'
# protocol = 'tcp'
tls_enabled: True

# Cria o aplicativo Flask
app = Flask(__name__)

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected to MQTT Broker!")
#         # Subscribe to topics here
#     else:
#         print(f"Failed to connect, rc: {rc}")

client = mqtt.Client()
client.connect(broker_address, port, keepalive=60)


# clientid = client

# Define a rota para receber o POST
@app.route("/", methods=[ "POST"])
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
    # client = mqtt.Client()
    # client.connect(broker_address, port)
    client.publish(topic, message)
    # client.disconnect()

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
