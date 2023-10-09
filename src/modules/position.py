from datetime import datetime

class Postion:
    """Classe para encapsular as posições obtidas via GPS"""
    
    @property
    def latitude(self) -> str:
        """Obtém o hash SHA-256 do endereço MAC do dispositivo"""
        return self.__latitude
    
    @property
    def longitude(self) -> str:
        """Obtém o hash SHA-256 do endereço MAC do dispositivo"""
        return self.__longitude
    
    @property
    def gps_time(self) -> datetime:
        """Obtém o hash SHA-256 do endereço MAC do dispositivo"""
        return self.__gps_time
    
    @property
    def gps_date(self) -> datetime:
        """Obtém o hash SHA-256 do endereço MAC do dispositivo"""
        return self.__gps_date