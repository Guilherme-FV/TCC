import paho.mqtt.client as mqtt
import numpy as np
import json
from os import environ
from math import radians, cos, sin, sqrt, atan2, degrees
from datetime import datetime

class LocationCombinator:
    def __init__(self, broker_address, topic):
        self.broker_address = broker_address
        self.topic = topic
        self.locations = []

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.start()

    def on_message(self, client, userdata, message):
        # Esta função é chamada quando uma nova mensagem é recebida
        payload = message.payload.decode('utf-8')
        payload_parsed = json.loads(payload)
        # print('Localização fornecida pelo módulo de colaboração' + str(payload_parsed['latitude']) + str(payload_parsed['longitude']))
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
    
    def calcular_media_cartesiana(self):
        # Converter de latitude e longitude para coordenadas cartesianas
        localizacoes = self.locations
        coordenadas_cartesianas = []
        for lat, lon in localizacoes:
            # Converter graus para radianos
            lat_rad = radians(lat)
            lon_rad = radians(lon)

            # Raio da Terra em km
            raio_terra = 6371.0

            # Converter para coordenadas cartesianas
            x = raio_terra * cos(lat_rad) * cos(lon_rad)
            y = raio_terra * cos(lat_rad) * sin(lon_rad)
            coordenadas_cartesianas.append((x, y))

        # Calcular a média das coordenadas cartesianas
        media_x = sum(x for x, _ in coordenadas_cartesianas) / len(coordenadas_cartesianas)
        media_y = sum(y for _, y in coordenadas_cartesianas) / len(coordenadas_cartesianas)

        # Converter a média de volta para latitude e longitude
        media_lon = atan2(media_y, media_x)
        media_lat = atan2(sqrt(media_x ** 2 + media_y ** 2), raio_terra)

        # Converter de radianos para graus
        media_lat = degrees(media_lat)
        media_lon = degrees(media_lon)

        combined_locations = {
            'veiculo_id': environ["BUSID"],
            'latitude': str(media_lat),
            'longitude': str(media_lon),
            'data': str(datetime.now().date()),
            'hora': str(datetime.now().time())
        }

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
