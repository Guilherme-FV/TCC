from datetime import datetime
from errno import EEXIST
from os import makedirs, path
from multiprocessing import Manager, Process
import sys

import modules


if __name__ == "__main__":
    killer = modules.System_Killer()
          
    if not path.exists(path.dirname(modules.TCPDUMP_LOG)):
        try:
            makedirs(path.dirname(modules.TCPDUMP_LOG))
        except OSError as exc:
            if exc.errno != EEXIST:
                raise

    # Requisitar ID do ônibus

    enter_devices = Manager().dict()
    exit_devices = Manager().dict()

    position_timer = datetime.now()
    ocupation_timer = datetime.now()

    device_scanner = Process(target=modules.live_device_scanner, args=(enter_devices,))
    position_tracker = Process(target=modules.position_ping)
    ocupation_tracker = Process(target=modules.get_bus_ocupation, args=(enter_devices, exit_devices))

    device_scanner.start()
    position_tracker.start()
    ocupation_tracker.start()

    while True:
        while killer.kill_now:
            print('TERMINANDO O PROGRAMA')
            device_scanner.terminate()
            print('TERMINANDO O DEVICE')
            device_scanner.join()
            print('DEVICE JOIN')
            position_tracker.terminate()
            print('TERMINANDO O POSITION')
            position_tracker.join()
            print('POSITION JOIN')
            ocupation_tracker.terminate()
            print('TERMINANDO O OCUPATION')
            ocupation_tracker.join()
            print('OCUPATION JOIN')
            sys.exit(0)
