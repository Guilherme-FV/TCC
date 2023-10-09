from datetime import datetime
import paho.mqtt.client as paho
import json
from modules.device import Device
from modules.position import Postion


def publish_position(position: Postion):
    client = paho.Client()
    if client.connect('54.207.195.3', 1883, 60) != 0:
        print('Não foi possível se conectar ao broker MQTT do módulo de coleta')
    
    position_package = {
        'latitude': position.latitude,
        'longitude': position.latitude,
        'data': position.gps_date,
        'tempo': position.gps_time
    }
    client.publish('position', json.dumps(position_package), 0)
    client.disconnect()

def publish_num_passengers(num_passengers: int, date_time: datetime):
    client = paho.Client()
    if client.connect('54.207.195.3', 1883, 60) != 0:
        print('Não foi possível se conectar ao broker MQTT do módulo de recebimento')
    
    num_passengers_package = {
        'lotacao': num_passengers,
        'data': date_time.date(),
        'tempo': date_time.time()
    }
    client.publish('num_passengers', json.dumps(num_passengers_package), 0)
    client.disconnect()

def publish_inactive_devices(inactive_devices):
    client = paho.Client()
    if client.connect('54.207.195.3', 1883, 60) != 0:
        print('Não foi possível se conectar ao broker MQTT do módulo de recebimento')
    
    inactive_devices_list = []
    for device in inactive_devices:
        inactive_devices_list.append(device.device_to_JSON())
    
    client.publish('exit_devices', json.dumps(inactive_devices_list, indent=4), 0)
    client.disconnect()
