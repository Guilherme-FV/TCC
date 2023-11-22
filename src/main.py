from datetime import datetime
from errno import EEXIST
from os import makedirs, path, environ
from multiprocessing import Manager, Process, Semaphore
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

    if "BUSID" in environ:
        BUS_ID = environ["BUSID"]
    else:
        BUS_ID = -1

    enter_devices = Manager().dict()
    exit_devices = Manager().dict()
    gps_semaphore = Semaphore(1)

    position_timer = datetime.now()
    ocupation_timer = datetime.now()

    device_scanner = Process(target=modules.live_device_scanner, args=(enter_devices, gps_semaphore))
    position_tracker = Process(target=modules.position_ping, args=(gps_semaphore,))
    ocupation_tracker = Process(target=modules.get_bus_ocupation, args=(enter_devices, exit_devices))

    device_scanner.start()
    position_tracker.start()
    ocupation_tracker.start()

    print(f'{datetime.now().time()} EXECUTANDO O PROGRAMA')
    
    while True:
        while killer.kill_now:
            print('ENCERRANDO O PROGRAMA...')
            device_scanner.terminate()
            print('ENCERRANDO A CONTAGEM DE DISPOSITIVOS...')
            device_scanner.join()
            position_tracker.terminate()
            print('ENCERRANDO RASTREAMENTO DO VEÍCULO...')
            position_tracker.join()
            ocupation_tracker.terminate()
            print('ENCERRANDO MONITORAMENTO DA LOTAÇÃO...')
            ocupation_tracker.join()
            sys.exit(0)
