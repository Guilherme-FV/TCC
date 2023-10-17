from shutil import move
from time import sleep, strftime
from datetime import datetime
from hashlib import sha256
from os import devnull, path
from subprocess import Popen
from signal import SIGTERM
from multiprocessing import Manager
import sys

from modules.system_killer import System_Killer
from modules.log_handler import TCPDUMP_LOG, follow_tcpdump_log, extract_probe_request_frame
from modules.device import Device
from modules.mqtt_client_handler import publish_position, publish_num_passengers


POSITION_TIMER_SECONDS = 60
OCUPATION_TIMER_SECONDS = 240

def tcpdump_start() -> Popen:
    """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
    with open(TCPDUMP_LOG, 'w', encoding='utf-8') as tcpdump_log:
        tcp_args = ['tcpdump', '-i', 'wlan0mon', '-e', '-ttt', '-U', 'wlan[0]=0x80', 'or', 'wlan[0]=0x40', 'or', 'wlan[0]=0x50']
        with Popen(tcp_args, stdout = tcpdump_log, stderr = open(devnull, 'w', encoding='utf-8')) as tcpdump_process:
            return tcpdump_process

def tcpdump_stop(tcpdump_process: Popen):
    """Finaliza o processo tcpdump e salva o arquivo atual de captura"""
    tcpdump_process.send_signal(SIGTERM)
    tcpdump_process.communicate()

    timestr = strftime('%Y-%m-%d_%H-%M')
    dump_filename = f'Capture_{timestr}.txt'
    dump_full_path = path.join(path.dirname(TCPDUMP_LOG), 'dump', dump_filename)
    
    try:
        move(TCPDUMP_LOG, dump_full_path)
    except IOError:
        pass

def live_device_scanner(enter_devices: Manager().dict()):
    """Varre constantemente o arquivo de log do tcpdump e cadastra/atualiza os dispositivos dentro do ônibus"""
    loglines = follow_tcpdump_log()
    tcpdump_process =  tcpdump_start()

    for line in loglines:
        frame = extract_probe_request_frame(line)
        if frame:
            frame_mac_hash = sha256(frame[0].encode('utf-8')).hexdigest()
            if frame_mac_hash in enter_devices:
                live_device = enter_devices[frame_mac_hash]
                live_device.last_seen = datetime.now()
            else:
                new_device = Device(frame[0], frame[1], 'first_seen_position')
                enter_devices[new_device.mac_hash] = new_device
    tcpdump_stop(tcpdump_process)

def position_ping():
    """Obtém a localização e o datetime atual e envia as informações para o banco de dados"""
    killer = System_Killer()
    while True:
        if killer.kill_now:
            sys.exit(0)
        sleep(POSITION_TIMER_SECONDS)
        # Pega latitude e longitude do GPS
        actual_datetime = datetime.now()
        publish_position('latitude', 'longitude', actual_datetime.date(), actual_datetime.time())

def live_devices_cleanup(enter_devices: Manager().dict(), exit_devices: Manager().dict()):
    """Verifica dispositivos que não são vistos a muito tempo e adiciona-os a lista dos que saíram do ônibus"""
    for device in enter_devices.values():
        if device.timeout():
            exit_devices[device.mac_hash] = device
            # Enviar infos para o banco de dados (assync de preferência)

def get_bus_ocupation(enter_devices: Manager().dict(), exit_devices: Manager().dict()):
    """Envia para o banco de dados a lotação atual do ônibus"""
    killer = System_Killer()
    while True:
        if killer.kill_now:
            sys.exit(0)
        sleep(OCUPATION_TIMER_SECONDS)
        live_devices_cleanup(enter_devices, exit_devices)
        bus_ocupation = len(enter_devices) - len(exit_devices)
        publish_num_passengers(bus_ocupation, datetime.now())
