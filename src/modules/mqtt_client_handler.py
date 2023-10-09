import paho.mqtt.client as paho
import json
from device import Device


def publish_position(latitude, longitude, date, time):
    client = paho.Client()
    if client.connect('localhost', 1883, 60) != 0:
        print('Não foi possível se conectar ao broker MQTT do módulo de coleta')
    
    position_package = {
        'latitude': latitude,
        'longitude': longitude,
        'data': date,
        'tempo': time
    }
    client.publish('fwd/position', json.dumps(position_package), 0)
    client.disconnect()

def publish_num_passengers(num_passengers, date, time):
    client = paho.Client()
    if client.connect('54.207.140.24', 1883, 60) != 0:
        print('Não foi possível se conectar ao broker MQTT do módulo de recebimento')
    
    num_passengers_package = {
        'lotacao': num_passengers,
        'data': date,
        'tempo': time
    }
    client.publish('num_passengers', json.dumps(num_passengers_package), 0)
    client.disconnect()

def publish_inactive_devices(inactive_devices):
    client = paho.Client()
    if client.connect('54.207.140.24', 1883, 60) != 0:
        print('Não foi possível se conectar ao broker MQTT do módulo de recebimento')
    
    inactive_devices_list = []
    for device in inactive_devices:
        inactive_devices_list.append(device.device_to_JSON())
    
    client.publish('exit_devices', json.dumps(inactive_devices_list, indent=4), 0)
    client.disconnect()
