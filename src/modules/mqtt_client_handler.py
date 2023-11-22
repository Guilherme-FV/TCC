from datetime import datetime
from time import sleep
from typing import List
from os import environ
import paho.mqtt.client as paho
import json
import requests

from modules.device import Device
from modules.location_combinator import LocationCombinator

RECEIVING_MODULE_IP = '15.229.35.41'
COLLECTION_MODULE_IP = 'localhost'

def publish_message(broker: str, topic: str, message: str, qos: int):
    client = paho.Client()
    if client.connect(broker, 1883, 60) != 0:
        print(f'Não foi possível se conectar ao broker MQTT {broker}')
    if broker == RECEIVING_MODULE_IP and not have_internet_connection():
        publish_3g_down(topic, message, qos)
        client.disconnect()
        return
    
    client.publish(topic, message, qos)
    client.disconnect()

def publish_position(latitude: float, longitude: float, gps_datetime: datetime):   
    position_package = {
        'veiculo_id': environ["BUSID"],
        'latitude': str(latitude),
        'longitude': str(longitude),
        'data': str(gps_datetime.date()),
        'hora': str(gps_datetime.time())
    }
    print(f'{datetime.now().time()} Publicando localização fornecida pelo GPS embarcado')
    publish_message(RECEIVING_MODULE_IP, 'position', json.dumps(position_package), 0)

def publish_num_passengers(num_passengers: int, date_time: datetime):
    num_passengers_package = {
        'veiculo_id': environ["BUSID"],
        'lotacao': num_passengers,
        'data': str(date_time.date()),
        'hora': str(date_time.time())
    }
    print(f'{datetime.now().time()} Publicando lotação: {num_passengers}')
    publish_message(RECEIVING_MODULE_IP, 'num_passengers', json.dumps(num_passengers_package), 0)

def publish_inactive_devices(inactive_devices: List[Device]):
    inactive_devices_list = []
    for device in inactive_devices:
        inactive_devices_list.append(device.device_to_JSON())
    print(f'{datetime.now().time()} Publicando dispositivos ausentes')
    publish_message(RECEIVING_MODULE_IP, 'exit_devices', json.dumps(inactive_devices_list), 0)

def publish_3g_down(topic, message, qos):
    print(f'{datetime.now().time()} Sem conexão com a internet')
    data = {
        "topic": topic,
        "message": message,
        "qos": qos
    }
    print(f'{datetime.now().time()} Solicitando publicação de uma mensagem no tópico: {topic}')
    publish_message(COLLECTION_MODULE_IP, '3gdown', json.dumps(data), 0)

def have_internet_connection():
    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    return False

def publish_gps_down():
    print(f'{datetime.now().time()} Sem sinal de GPS')
    publish_message(COLLECTION_MODULE_IP, 'gpsdown', '1', 0)
    print(f'{datetime.now().time()} Solicitando localização')
    message_collector = LocationCombinator(COLLECTION_MODULE_IP, 'positionColab')
    sleep(10)
    if len(message_collector.locations) != 0:
        print(f'Localizações recebidas: {len(message_collector.locations)}')
        print(f'{datetime.now().time()} Publicando localização fornecida via Módulo de colaboração: {message_collector.calcular_media_cartesiana()}')
        publish_message(RECEIVING_MODULE_IP, 'position', message_collector.calcular_media_cartesiana(), 0)
        message_collector.stop()
    
