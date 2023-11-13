from datetime import datetime, timedelta
import serial
from serial import Serial
from pynmea2 import parse
from multiprocessing import Process


class GPSHandler:

    def __init__(self):
        self.__status = 'V'
        self.__latitude = 0
        self.__longitude = 0
        self.__date_time = datetime.now()

    @property
    def latitude(self) -> float:
        return self.__latitude
    
    @latitude.setter
    def latitude(self, new_latitude: float):
        self.__latitude = new_latitude
    
    @property
    def longitude(self) -> float:
        return self.__longitude
    
    @longitude.setter
    def longitude(self, new_longitude: float):
        self.__longitude = new_longitude
    
    @property
    def date_time(self) -> datetime:
        return self.__date_time
    
    @date_time.setter
    def date_time(self, new_datetime: datetime):
        self.__date_time = new_datetime
    
    @property
    def status(self) -> bool:
        return self.__status == 'A'
    
    @status.setter
    def status(self, new_status: str):
        self.__status = new_status

    def __str__(self) -> str:
        return f'Latitude: {self.latitude}, Longitude: {self.longitude}, Datetime: {self.date_time} Status: {self.status}'

def get_gps_data(gps_semaphore) -> GPSHandler:
    with gps_semaphore:
        gps_data = GPSHandler()
        gps_serial = Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.5)
        try:
            while True:
                nmea_sentence = gps_serial.readline().decode('latin-1')
                if nmea_sentence.startswith('$GPRMC'):
                    parsed_sentance = parse(nmea_sentence)
                    gps_data.status = parsed_sentance.status
                    if gps_data.status:
                        gps_data.latitude = parsed_sentance.latitude
                        gps_data.longitude = parsed_sentance.longitude
                        gps_data.date_time = datetime.combine(parsed_sentance.datestamp, parsed_sentance.timestamp) - timedelta(hours = 3)
                    return gps_data
        except serial.SerialException:
            print('ERRO NA SERIAL DO GPS')
        finally:
            gps_serial.close()