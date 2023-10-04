from errno import EEXIST
from os import makedirs, path
from multiprocessing import Manager, Process

from modules.log_handler import *
from modules.system_killer import System_Killer
from modules.bus_device_tracker import get_bus_ocupation, live_device_scanner, position_ping, POSITION_TIMER_SECONDS, OCUPATION_TIMER_SECONDS


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

    position_timer = datetime.now()
    ocupation_timer = datetime.now()

    device_scanner = Process(target=live_device_scanner, args=(enter_devices,))
    position_tracker = Process(target=position_ping)
    ocupation_tracker = Process(target=get_bus_ocupation, args=(enter_devices, exit_devices))

    device_scanner.start()
    position_tracker.start()
    position_tracker.start()
    
    while True:
        if killer.kill_now:
            print('TERMINANDO O PROGRAMA')
            raise SystemExit
