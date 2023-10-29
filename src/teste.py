from hashlib import sha256
from multiprocessing import Manager
from time import sleep
from modules.bus_device_tracker import live_devices_cleanup

from modules.device import Device
from modules.log_handler import TCPDUMP_LOG, extract_probe_request_frame


def live_device_scanner(enter_devices: dict[str, Device]):
    """Varre constantemente o arquivo de log do tcpdump e cadastra/atualiza os dispositivos dentro do ônibus"""
    with open(TCPDUMP_LOG, 'r', encoding='utf-8') as log_file:
        for line in log_file.readlines():
            frame = extract_probe_request_frame(line)
            if frame:
                frame_mac_hash = sha256(frame[0].encode('utf-8')).hexdigest()
                if frame_mac_hash in enter_devices:
                    live_device = enter_devices[frame_mac_hash]
                    live_device.seen()
                    print(f'Dispositivo {live_device} visto novamente')
                else:
                    new_device = Device(frame[0], frame[1])
                    enter_devices[new_device.mac_hash] = new_device
                    print(f'Dispositivo {new_device} visto pela primeira vez')
                
enter_devices = Manager().dict()
exit_devices = Manager().dict()
live_device_scanner(enter_devices)
while True:
    live_devices_cleanup(enter_devices, exit_devices)
    print(len(enter_devices))
    print(len(exit_devices))
    sleep(3)