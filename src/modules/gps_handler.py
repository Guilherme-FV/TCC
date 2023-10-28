from serial import Serial
from pynmea2 import parse
from multiprocessing import Process


class GPSHandler:

    GPS_SERIAL = Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.5)

    def __init__(self):
        self.__status = 'V'
        self.__latitude = ''
        self.__longitude = ''
        self.__timestamp = ''
        self.__datestamp = ''
        self.__gps_process = Process(target=self.update_data)
        self.gps_process.start()

    def update_data(self):
        while True:
            serial_line = self.GPS_SERIAL.readline().decode('latin-1')
            print(serial_line)
            if serial_line.startswith('$GPRMC'):
                gps_data = parse(serial_line)
                self.__status = gps_data.status
                if self.status:
                    self.__latitude = gps_data.latitude
                    self.__longitude = gps_data.longitude
                    self.__timestamp = gps_data.timestamp
                    self.__datestamp = gps_data.datestamp

    @property
    def gps_process(self) -> Process:
        return self.__gps_process

    @property
    def latitude(self) -> str:
        return self.__latitude
    
    @property
    def longitude(self) -> str:
        return self.__longitude
    
    @property
    def timestamp(self) -> str:
        return self.__timestamp
    
    @property
    def datestamp(self) -> str:
        return self.__datestamp
    
    @property
    def status(self) -> bool:
        return self.__status == 'A'