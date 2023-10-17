from datetime import datetime
import paho.mqtt.client as paho
import json
from modules.device import Device
from modules.position import Postion

RECEIVING_MODULE_IP = '54.207.195.3'
COLLECTION_MODULE_IP = 'localhost'

def publish_message(broker: str, topic: str, message: str, qos: int):
    client = paho.Client()
    if client.connect(broker, 1883, 60) != 0:
        print(f'Não foi possível se conectar ao broker MQTT {broker}')
    
    client.publish(topic, message, qos)
    client.disconnect()

def publish_position(position: Postion):   
    position_package = {
        'latitude': position.latitude,
        'longitude': position.latitude,
        'data': position.gps_date,
        'tempo': position.gps_time
    }
    publish_message(RECEIVING_MODULE_IP, 'position', json.dumps(position_package), 0)

def publish_num_passengers(num_passengers: int, date_time: datetime):
    num_passengers_package = {
        'lotacao': num_passengers,
        'data': date_time.date(),
        'tempo': date_time.time()
    }
    publish_message(RECEIVING_MODULE_IP, 'num_passengers', json.dumps(num_passengers_package), 0)

def publish_inactive_devices(inactive_devices):
    inactive_devices_list = []
    for device in inactive_devices:
        inactive_devices_list.append(device.device_to_JSON())
    
    publish_message(RECEIVING_MODULE_IP, 'exit_devices', json.dumps(inactive_devices_list, indent=4), 0)

def pubish_3g_down():
    publish_message(COLLECTION_MODULE_IP, 'local/3gdown', '1', 0)

def pubish_gps_down():
    publish_message(COLLECTION_MODULE_IP, 'local/gpsdown', '1', 0)