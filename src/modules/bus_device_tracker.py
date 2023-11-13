from shutil import move
from time import sleep, strftime
from datetime import datetime
from hashlib import sha256
from os import devnull, path
from subprocess import Popen
from signal import SIGTERM
from multiprocessing import Manager
import sys
from modules.gps_handler import get_gps_data

from modules.system_killer import System_Killer
from modules.log_handler import TCPDUMP_LOG, follow_tcpdump_log, extract_probe_request_frame
from modules.device import Device
from modules.mqtt_client_handler import publish_position, publish_num_passengers, publish_gps_down, publish_inactive_devices


POSITION_TIMER_SECONDS = 30
OCUPATION_TIMER_SECONDS = 45

def tcpdump_start() -> Popen:
    """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
    tcp_args = ['sudo', 'tcpdump', '-i', 'wlan1', '-e', '-tttt', '-U', 'wlan[0]=0x40']
    return Popen(tcp_args, stdout = open(TCPDUMP_LOG, 'w', encoding='utf-8'), stderr = open(devnull, 'w', encoding='utf-8'))

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

def live_device_scanner(enter_devices: dict[str, Device]):
    """Varre constantemente o arquivo de log do tcpdump e cadastra/atualiza os dispositivos dentro do ônibus"""
    loglines = follow_tcpdump_log()
    tcpdump_process =  tcpdump_start()

    for line in loglines:
        frame = extract_probe_request_frame(line)
        if frame:
            frame_mac_hash = sha256(frame[0].encode('utf-8')).hexdigest()
            if frame_mac_hash in enter_devices:
                enter_devices[frame_mac_hash].seen()
                print(f'DISPOSITIVO: {frame[0]} VISTO NOVAMENTE')
            else:
                new_device = Device(frame[0], frame[1])
                enter_devices[new_device.mac_hash] = new_device
                print(f'NOVO DISPOSITIVO: {frame[0]}')
    tcpdump_stop(tcpdump_process)

def position_ping():
    """Obtém a localização e o datetime atual e envia as informações para o banco de dados"""
    killer = System_Killer()
    while True:
        try:
            if killer.kill_now:
                sys.exit(0)
            sleep(POSITION_TIMER_SECONDS)
            gps_data = get_gps_data()
            if gps_data.status == True:
                publish_position(gps_data.latitude, gps_data.longitude, gps_data.date_time)
            else:
                publish_gps_down()
        except KeyboardInterrupt:
            gps_data = get_gps_data()
            if gps_data.status == True:
                publish_position(gps_data.latitude, gps_data.longitude, gps_data.date_time)
            if killer.kill_now:
                sys.exit(0)

def live_devices_cleanup(enter_devices: dict[str, Device], exit_devices: dict[str, Device]):
    """Verifica dispositivos que não são vistos a muito tempo e adiciona-os a lista dos que saíram do ônibus"""
    inactive_devices = []
    for device in enter_devices.values():
        if exit_devices.get(device.mac_hash) is None:
            if device.timeout():
                if device.first_seen == device.last_seen:
                    del enter_devices[device.mac_hash]
                    continue
                exit_devices[device.mac_hash] = device
                print(f'DISPOSITIVO: {device.mac_hash} REMOVIDO')
                inactive_devices.append(device)
    if len(inactive_devices) != 0:
        publish_inactive_devices(inactive_devices)

def get_bus_ocupation(enter_devices: dict[str, Device], exit_devices: dict[str, Device]):
    """Envia para o banco de dados a lotação atual do ônibus"""
    killer = System_Killer()
    while True:
        try:
            if killer.kill_now:
                sys.exit(0)
            sleep(OCUPATION_TIMER_SECONDS)
            live_devices_cleanup(enter_devices, exit_devices)
            bus_ocupation = len(enter_devices) - len(exit_devices)
            publish_num_passengers(bus_ocupation, datetime.now())
        except KeyboardInterrupt:
            live_devices_cleanup(enter_devices, exit_devices)
            bus_ocupation = len(enter_devices) - len(exit_devices)
            publish_num_passengers(bus_ocupation, datetime.now())
            if killer.kill_now:
                sys.exit(0)