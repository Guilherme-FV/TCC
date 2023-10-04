import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from datetime import datetime
from errno import EEXIST
from hashlib import sha256
from multiprocessing import Manager, Process
from time import sleep
from os import makedirs, path
from threading import Thread
from random import randint

from src.modules.log_handler import *
from src.modules.device import Device
from src.modules.system_killer import System_Killer

def device_scanner_function(enter_devices):
    loglines = follow_tcpdump_log()
    for line in loglines:
        frame = extract_probe_request_frame(line)
        if frame:
            frame_mac_hash = sha256(frame[0].encode('utf-8')).hexdigest()
            if frame_mac_hash in enter_devices:
                live_device = enter_devices[frame_mac_hash]
                live_device.last_seen = datetime.now()
                print(f'ATUALIZANDO LAST SEEN DO DISPOSITIVO: {enter_devices[frame_mac_hash]}')
            else:
                new_device = Device(frame[0], frame[1])
                enter_devices[new_device.mac_hash] = new_device
                print(f'NOVO DISPOSITIVO DETECTADO {enter_devices[new_device.mac_hash]}')

def write_log_file():
    probe_number = 0
    while True:
        with open(TCPDUMP_LOG, 'a+') as log_file:
            if probe_number % 5 == 0:
                log_file.write(f'{current_date_time()} 10702424795us B 2437 MHz -76dBm signal BSSID:Broadcast DA:Broadcast SA:00:00:00:00:00:00 (oui Unknown) Probe Request () [1.0 2.0 5.5 11.0 Mbit]\n')
            else:
                log_file.write(f'{current_date_time()} 10702424795us B 2437 MHz -76dBm signal BSSID:Broadcast DA:Broadcast SA:{random_mac_address()} (oui Unknown) Probe Request () [1.0 2.0 5.5 11.0 Mbit]\n')
        probe_number += 1
        sleep(1)

def random_mac_address():
    mac_parts = [f'{randint(0, 255):02X}' for _ in range(6)]
    mac_address = ":".join(mac_parts)
    return mac_address

def current_date_time():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_datetime

def position_function():
    while True:
        sleep(10)
        print('---------------- COLETA DE GPS E ENVIO PARA BANCO DE DADOS ----------------')
    
def cleaup_function(enter_devices, exit_devices):
    for mac_hash, device in enter_devices.items():
        if device.timeout():
            exit_devices[device.mac_hash] = device
            print(f'DISPOSITIVO {device} ADICIONADO À LISTA DE DISPOSITIVOS AUSENTES')

def ocupation_function(enter_devices, exit_devices):
    while True:
        sleep(15)
        cleaup_function(enter_devices, exit_devices)
        bus_ocupation = len(enter_devices) - len(exit_devices)
        print(f'OCUPAÇÃO DO ÔNIBUS: {bus_ocupation}. ENVIADA PARA O BANCO DE DADOS') 


if __name__ == "__main__":
    """Início do programa"""

    killer = System_Killer()

    if not path.exists(path.dirname(TCPDUMP_LOG)):
        try:
            makedirs(path.dirname(TCPDUMP_LOG))
        except OSError as exc:
            if exc.errno != EEXIST:
                raise

    # Requisitar ID do ônibus

    enter_devices = Manager().dict()
    exit_devices = Manager().dict()

    p2_timer = datetime.now()
    p4_timer = datetime.now()

    p1 = Process(target=device_scanner_function, args=(enter_devices,))
    p2 = Process(target=position_function)
    p4 = Process(target=ocupation_function, args=(enter_devices, exit_devices))
    t1 = Thread(target=write_log_file)

    p1.start()
    sleep(1)
    t1.start()
    p2.start()
    p4.start()
    
    while True:
        if killer.kill_now:
            print('TERMINANDO O PROGRAMA')
            raise SystemExit
