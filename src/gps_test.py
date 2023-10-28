from time import sleep
from modules.gps_handler import GPSHandler

gps_handler = GPSHandler()
while True:
        print(f'Latitude: {gps_handler.latitude}, Longitude: {gps_handler.longitude}, Timestamp: {gps_handler.timestamp}, Datestamp: {gps_handler.datestamp}')
        sleep(1)