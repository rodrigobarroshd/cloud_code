import random
from flask import Flask
from flask_mqtt import Mqtt
import paho.mqtt.client as Mqtt
# from flask_socketio import SocketIO


app = Flask(__name__)
# use the free broker from HIVEMQ
app.config['MQTT_BROKER_URL'] = "jackal.rmq.cloudamqp.com"
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
# set the username here if you need authentication for the broker
app.config['MQTT_USERNAME'] = 'xyoowllx:xyoowllx'
# set the password here if the broker demands authentication
app.config['MQTT_PASSWORD'] = 'Gle6D-nfdPPGDfg-uLDfQLw9W349orBv'
# set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_KEEPALIVE'] = 5
# set TLS to disabled for testing purposes
app.config['MQTT_TLS_ENABLED'] = False

# mqtt = Mqtt.Client()

client_id = f'python-mqtt-{random.randint(0, 1000)}'
mqtt = Mqtt.Client(client_id)
def create_app():
    app = Flask(__name__)
    mqtt.init_app(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('home/mytopic')


# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
