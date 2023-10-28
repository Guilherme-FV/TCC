import serial
import pynmea2

from modules.gps_handler import get_gps_data

while True:
        gps_data = get_gps_data()
        print(type(gps_data.latitude), type(gps_data.longitude), type(gps_data.timestamp), type(gps_data.datestamp), type(gps_data.status))