import paho.mqtt.client as paho
import requests


RECEIVING_MODULE_IP = '15.229.35.41'

def publish_message(broker: str, topic: str, message: str, qos: int):
    client = paho.Client()
    try:
        if client.connect(broker, 1883, 60) != 0:
            print(f'Não foi possível se conectar ao broker MQTT {broker}')
        if broker == RECEIVING_MODULE_IP and not have_internet_connection():
            client.disconnect()
            return
    except Exception:
        if broker == RECEIVING_MODULE_IP and not have_internet_connection():
            print('aaaaaaaaaaaaaaaaaaaaa')
            client.disconnect()
            return
    
    client.publish(topic, message, qos)
    client.disconnect()


def have_internet_connection():
    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    return False


publish_message(RECEIVING_MODULE_IP, 'position', 'teste', 0)