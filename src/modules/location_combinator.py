import paho.mqtt.client as mqtt
import numpy as np
import json
from os import environ

class LocationCombinator:
    def __init__(self, broker_address, topic):
        self.broker_address = broker_address
        self.topic = topic
        self.locations = []

        self.client = mqtt.Client()
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        # Esta função é chamada quando uma nova mensagem é recebida
        payload = message.payload.decode('utf-8')
        payload_parsed = json.loads(payload)
        location = (float(payload_parsed['latitude']), float(payload_parsed['longitude']))
        self.locations.append(location)

    def combine_locations(self):
        if len(self.locations) == 0:
            return None

        latitudes = [coord[0] for coord in self.locations]
        longitudes = [coord[1] for coord in self.locations]

        combined_locations = {}
        combined_locations['veiculo_id'] = environ["BUSID"]
        combined_locations['latitude'] = np.mean(latitudes)
        combined_locations['longitude'] = np.mean(longitudes)

        return json.dumps(combined_locations)
        

    def start(self):
        # Conecta ao broker MQTT
        self.client.connect(self.broker_address)

        # Inscreve no tópico desejado
        self.client.subscribe(self.topic)

        # Inicia o loop de recepção de mensagens
        self.client.loop_start()

    def stop(self):
        # Para o loop e desconecta do broker MQTT
        self.client.loop_stop()
        self.client.disconnect()

    def print_locations(self):
        for location in self.locations:
            print(location)
