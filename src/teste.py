from os import devnull
import subprocess
from multiprocessing import Manager
from typing import Generator
from datetime import datetime
from hashlib import sha256
from modules.device import Device
from time import sleep
from modules.log_handler import TCPDUMP_LOG
from modules.system_killer import System_Killer

def live_device_scanner(enter_devices: Manager().dict()):
    """Varre constantemente o arquivo de log do tcpdump e cadastra/atualiza os dispositivos dentro do ônibus"""
    loglines = follow_tcpdump_log()
    tcpdump_process =  tcpdump_start()

    for line in loglines:
        frame = extract_probe_request_frame(line)
        print(line)
        print(frame)
        if frame:
            frame_mac_hash = sha256(frame[0].encode('utf-8')).hexdigest()
            if frame_mac_hash in enter_devices:
                live_device = enter_devices[frame_mac_hash]
                live_device.last_seen = datetime.now()
            else:
                new_device = Device(frame[0], frame[1], 'first_seen_position')
                enter_devices[new_device.mac_hash] = new_device

def follow_tcpdump_log() -> Generator[str, None, None]:
    """Função que captura inserções conforme alimentadas no log"""
    killer = System_Killer()
    with open(TCPDUMP_LOG, 'r', encoding='utf-8') as log_file:
        log_file.seek(0,2)
        while True:
            line = log_file.readline()
            if not line:
                sleep(0.1)
                if killer.kill_now:
                    return
                continue
            yield line

def extract_probe_request_frame(probe_request_frame: str):
    """Extrai o MAC e a datetime do probe request e retorna um array [MAC, datetime]"""
    
    if not probe_request_frame.strip():
        return None
    
    device_info = []
    try:
        mac = probe_request_frame.split(' SA:')[1][0:17]
        if len(mac) != 17:
            raise ValueError
        device_info.append(mac)
        device_info.append(datetime.strptime(probe_request_frame[0:19], '%Y-%m-%d %H:%M:%S'))
    except (ValueError, IndexError):
        pass
    else:
        return device_info

def tcpdump_start() -> subprocess.Popen:
    """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
    tcp_args = ['sudo', 'tcpdump', '-i', 'eth0', '-e', '-U']
    return subprocess.Popen(tcp_args, stdout = open(TCPDUMP_LOG, 'w', encoding='utf-8'), stderr = open(devnull, 'w', encoding='utf-8'))


if __name__ == "__main__":
    enter_devices = Manager().dict()
    live_device_scanner(enter_devices)
