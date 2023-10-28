from datetime import datetime, timedelta
from serial import Serial
from pynmea2 import parse
from multiprocessing import Process


class GPSHandler:

    def __init__(self):
        self.__status = 'V'
        self.__latitude = ''
        self.__longitude = ''
        self.__datetime = ''

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
    def datetime(self) -> datetime:
        return self.__datetime
    
    @datetime.setter
    def datetime(self, new_datetime: datetime):
        self.__datetime = new_datetime
    
    @property
    def status(self) -> bool:
        return self.__status == 'A'
    
    @status.setter
    def status(self, new_status: str):
        self.__status = new_status

    def __str__(self) -> str:
        return f'Latitude: {self.latitude}, Longitude: {self.longitude}, Datetime: {self.datetime} Status: {self.status}'

def get_gps_data():
        gps_data = GPSHandler()
        gps_serial = Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.5)
        while True:
            nmea_sentence = gps_serial.readline().decode('latin-1')
            if nmea_sentence.startswith('$GPRMC'):
                parsed_sentance = parse(nmea_sentence)
                gps_data.status = parsed_sentance.status
                if gps_data.status:
                    gps_data.latitude = parsed_sentance.latitude
                    gps_data.longitude = parsed_sentance.longitude
                    gps_data.datetime = datetime.combine(parsed_sentance.datestamp, parsed_sentance.timestamp) - timedelta(hours = 3)
                return gps_data