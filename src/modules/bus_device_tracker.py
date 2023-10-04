from signal import SIGTERM
from subprocess import Popen
from os import devnull, path
from shutil import move
from time import sleep, strftime
from datetime import datetime
from hashlib import sha256

from .log_handler import *
from .device import Device


POSITION_TIMER_SECONDS = 60
OCUPATION_TIMER_SECONDS = 240

def tcpdump_start(path = TCPDUMP_LOG) -> Popen:
    """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
    with open(path, 'w') as tcpdump_log:
        tcp_args = ['tcpdump', '-i', 'wlan0mon', '-e', '-ttt', '-U', 'wlan[0]=0x80', 'or', 'wlan[0]=0x40', 'or', 'wlan[0]=0x50']
        tcp_process = Popen(tcp_args, stdout = tcpdump_log, stderr = open(devnull, 'w'))
    return tcp_process

def tcpdump_stop(tcp_process, tcpdump_log_path = TCPDUMP_LOG):
    """Finaliza o processo tcpdump e salva o arquivo atual de captura"""
    tcp_process.send_signal(SIGTERM)
    tcp_process.communicate()

    timestr = strftime('%Y-%m-%d_%H-%M')
    dump_filename = f'Capture_{timestr}.txt'
    dump_full_path = path.join(path.dirname(tcpdump_log_path), 'dump', dump_filename)
    
    try:
        move(tcpdump_log_path, dump_full_path)
    except IOError:
        pass

def live_device_scanner(enter_devices):
    """Varre constantemente o arquivo de log do tcpdump e cadastra/atualiza os dispositivos dentro do ônibus"""
    loglines = follow_tcpdump_log()
    tcpdump_process = tcpdump_start()

    for line in loglines:        
        frame = extract_probe_request_frame(line)
        if frame:
            frame_mac_hash = sha256(frame[0].encode('utf-8')).hexdigest()
            if frame_mac_hash in enter_devices:
                live_device = enter_devices[frame_mac_hash]
                live_device.last_seen = datetime.now()
            else:
                new_device = Device(frame[0], frame[1])
                enter_devices[new_device.mac_hash] = new_device

def position_ping():
    """Obtém a localização e o datetime atual e envia as informações para o banco de dados"""
    while True:
        sleep(POSITION_TIMER_SECONDS)
        # Pega latitude e longitude do GPS
        actual_datetime = datetime.now()
        # Envia tudo para o banco de dados

def live_devices_cleanup(enter_devices, exit_devices):
    """Verifica dispositivos que não são vistos a muito tempo e adiciona-os a lista dos que saíram do ônibus"""
    for mac_hash, device in enter_devices.items():
        if device.timeout():
            exit_devices[device.mac_hash] = device
            # Enviar infos para o banco de dados (assync de preferência)

def get_bus_ocupation(enter_devices, exit_devices):
    """Envia para o banco de dados a lotação atual do ônibus"""
    while True:
        sleep(OCUPATION_TIMER_SECONDS)
        live_devices_cleanup(enter_devices, exit_devices)
        bus_ocupation = len(enter_devices) - len(exit_devices)
        # Enviar dados de lotação para o banco de dados