from datetime import datetime
from multiprocessing import Semaphore
from modules.device import Device


gpsSemaphore = Semaphore(1)

device = Device('12:12:12:12:12:12', datetime.now(), gpsSemaphore)

print(device.device_to_JSON())