from flask import Flask, request
import json
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, broker_address, port, username, password):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.port = port
        self.username = username
        self.password = password

        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_address, self.port, keepalive=60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT com sucesso!")
        else:
            print(f"Falha ao conectar, código de erro: {rc}")

    def on_publish(self, client, userdata, mid):
        print("Mensagem publicada!")

    def publish_message(self, topic, payload):
        print(f"Tópico: {topic}, Payload: {payload}")
        self.client.publish(topic, payload)


class FlaskApp:
    def __init__(self, mqtt_client):
        self.app = Flask(__name__)
        self.mqtt_client = mqtt_client
        self.app.add_url_rule("/", "receive_message",
                              self.receive_message, methods=["POST"])

    def receive_message(self):
        message_json = request.get_json()
        self.process_message(message_json)
        return json.dumps({"mensagem": "Mensagem recebida e publicada com sucesso!"})

    def process_message(self, message_json):
        try:
            if isinstance(message_json, dict):
                topic = list(message_json.keys())[0]
                payload = list(message_json.items())[1][1]
                self.mqtt_client.publish_message(topic, payload)
            else:
                raise TypeError("Mensagem JSON deve ser um dicionário.")
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == "__main__":
    broker_address = "jackal.rmq.cloudamqp.com"
    port = 1883
    username = 'spiusnlq:spiusnlq'
    password = 'H42vRkntxAQrhkZtTZwXrLvWXYg5OpWH'

    mqtt_client = MQTTClient(broker_address, port, username, password)
    flask_app = FlaskApp(mqtt_client)
    flask_app.run()
