import serial
import pynmea2

from modules.gps_handler import get_gps_data

while True:
        print(get_gps_data())