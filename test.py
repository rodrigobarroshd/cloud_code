from flask import Flask, request, jsonify
import paho.mqtt.publish as publish
import json

app = Flask(__name__)


broker = 'jackal.rmq.cloudamqp.com'
port = 1883
# topic = "python/mqtt"
client_id = 'microbot_client'
username = 'xyoowllx:xyoowllx'
password = 'Gle6D-nfdPPGDfg-uLDfQLw9W349orBv'

@app.route('/', methods=['POST'])
def enviar_mensagem():
    # Recebe a mensagem JSON do cliente
    dados = request.json

    # Extrai o tópico e a mensagem da mensagem JSON
    topico = list(dados.keys())[0]
    mensagem = dados[topico]
    

    # Envia a mensagem para o MQTT no respectivo tópico
    publish.single(topico, mensagem, hostname='mqtt.eclipse.org')

    return jsonify({'mensagem': 'Mensagem enviada para o tópico MQTT'}), 200

if __name__ == '__main__':
    app.run(debug=True)
