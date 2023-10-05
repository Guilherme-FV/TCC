from datetime import datetime
from os import path
from time import sleep
from os import path

from .system_killer import System_Killer


TCPDUMP_LOG = path.join('logs', 'tcpdump.txt')

def extract_probe_request_frame(probe_request_frame):
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

def follow_tcpdump_log():
    """Função que captura inserções conforme alimentadas no log"""
    killer = System_Killer()
    log_file = open(TCPDUMP_LOG, 'r')
    log_file.seek(0,2)
    while True:
        line = log_file.readline()
        if not line:
            sleep(0.1)
            if killer.kill_now:
                return
            continue
        yield line
