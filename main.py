from flask import Flask, jsonify, request
import paho.mqtt.publish as publish
import json
from paho.mqtt import client as mqtt_client
app = Flask(__name__)


broker = 'jackal.rmq.cloudamqp.com'
port = 1883
topic = "URA001/teste"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt'
username = 'xyoowllx:xyoowllx'
password = 'Gle6D-nfdPPGDfg-uLDfQLw9W349orBv'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client








livros = [
    {
        'id': 1,
        'título': 'O Senhor dos Anéis - A Sociedade do Anel',
        'autor': 'J.R.R Tolkien'
    },
    
]

# Consultar(todos)
@app.route('/livros',methods=['GET'])
def obter_livros():
    return jsonify(livros)

# Consultar(id)
@app.route('/livros/<int:id>',methods=['GET'])
def obter_livro_por_id(id):
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)
# Editar
@app.route('/livros/<int:id>',methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            livros[indice].update(livro_alterado)
            return jsonify(livros[indice])
# Criar
@app.route('/livros',methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()
    livros.append(novo_livro)
    
    return jsonify(livros)



@app.route('/receber', methods=['GET', 'POST'])
def enviar_mensagem():
    # Recebe a mensagem JSON do cliente
    dados = request.json

    # Extrai o tópico e a mensagem da mensagem JSON
    topico = list(dados.keys())[0]
    mensagem = dados[topico]
    

    # Envia a mensagem para o MQTT no respectivo tópico
    # publish.single(topico, mensagem, hostname= broker)
    publish.single(topico, json.dumps(mensagem), hostname='jackal.rmq.cloudamqp.com/1883', auth={'username': username, 'password': password})

    return jsonify({'mensagem': 'Mensagem enviada para o tópico MQTT'}), 200



    
app.run(port=5000,host='localhost',debug=True)

