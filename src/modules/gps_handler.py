from serial import Serial
from pynmea2 import parse
from multiprocessing import Process


class GPSHandler:

    def __init__(self):
        self.__status = 'V'
        self.__latitude = ''
        self.__longitude = ''
        self.__timestamp = ''
        self.__datestamp = ''

    @property
    def latitude(self) -> str:
        return self.__latitude
    
    @latitude.setter
    def latitude(self, new_latitude):
        self.__latitude = new_latitude
    
    @property
    def longitude(self) -> str:
        return self.__longitude
    
    @longitude.setter
    def longitude(self, new_longitude):
        self.__longitude = new_longitude
    
    @property
    def timestamp(self) -> str:
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, new_timestamp):
        self.__timestamp = new_timestamp
    
    @property
    def datestamp(self) -> str:
        return self.__datestamp
    
    @datestamp.setter
    def datestamp(self, new_datestamp):
        self.__datestamp = new_datestamp
    
    @property
    def status(self) -> bool:
        return self.__status == 'A'
    
    @status.setter
    def status(self, new_status):
        self.__status = new_status

    def __str__(self) -> str:
        return f'Latitude: {self.latitude}, Longitude: {self.longitude}, Timestamp: {self.timestamp}, Datestamp: {self.datestamp}, Status: {self.status}'

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
                    gps_data.timestamp = parsed_sentance.timestamp
                    gps_data.datestamp = parsed_sentance.datestamp
                return gps_data