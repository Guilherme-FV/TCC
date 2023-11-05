from datetime import datetime
from hashlib import sha256
from modules.gps_handler import GPSHandler, get_gps_data


class Device:
    """Classe para criar dispositvos detecdados"""

    # Quantidade de segundos necessários para que um dispositivo seja considerado fora do ônibus
    TIMEOUT_SECONDS = 60
    
    def __init__(self, mac: str, first_seen: datetime):
        """Cria um objeto a partir do endereço MAC do dispositivo e da primeira vez que o dispositivo foi detectado em uma varredura"""
        # Usando SHA256 para anonimizar o endereço MAC
        self.__mac_hash = sha256(mac.encode('utf-8')).hexdigest()
        self.__first_seen = first_seen
        self.__last_seen = first_seen
        self.__first_seen_position = GPSHandler()#get_gps_data()
        self.__last_seen_position = self.first_seen_position


    def timeout(self) -> bool:
        """Verifica se o dispositivo está fora do ônibus"""
        if (datetime.now() - self.last_seen).total_seconds() > self.TIMEOUT_SECONDS:
            return True
        return False
    
    def device_to_JSON(self) -> dict[str, str]:
        """Retorna todos os atributos do dispositivo em formato JSON"""
        attributes = {
            'mac_hash': self.__mac_hash,
            'entrada': str(self.__first_seen.strftime("%H:%M:%S")),
            'saida': str(self.__last_seen.strftime("%H:%M:%S")),
            'data_entrada': str(self.__first_seen.date()),
            'data_saida': str(self.__last_seen.date()),
            'posicao_entrada': str(self.__first_seen_position),
            'posicao_saida': str(self.__last_seen_position)
        }
        return attributes
    
    def seen(self):
        self.last_seen = datetime.now()
        self.last_seen_position = GPSHandler()#get_gps_data()
    
    @property
    def mac_hash(self) -> str:
        """Obtém o hash SHA-256 do endereço MAC do dispositivo"""
        return self.__mac_hash
        
    @property
    def first_seen(self) -> datetime:
        """Obtém a primeira vez que o dispositivo foi detectado em uma varredura"""
        return self.__first_seen
    
    @property
    def last_seen(self) -> datetime:
        """Obtém a última vez que o dispositivo foi detectado em uma varredura"""
        return self.__last_seen
    
    @last_seen.setter
    def last_seen(self, new_last_seen : datetime):
        """Define a última vez que o dispositivo foi detectado em uma varredura"""
        self.__last_seen = new_last_seen

    @property
    def first_seen_position(self) -> GPSHandler:
        """Obtém a localização da primeira vez que o dispositivo foi detectado em uma varredura"""
        return self.__first_seen_position
    
    @property
    def last_seen_position(self) -> GPSHandler:
        """Obtém a localização da última vez que o dispositivo foi detectado em uma varredura"""
        return self.__last_seen_position
    
    @last_seen_position.setter
    def last_seen_position(self, new_last_seen_position : GPSHandler):
        """Define a última vez que o dispositivo foi detectado em uma varredura"""
        self.__last_seen_position = new_last_seen_position
    
    
    def __str__(self) -> str:
        """Retorna uma representação em string do objeto"""
        return f'MAC_HASH: {self.__mac_hash} | First Seen: {self.__first_seen} | Last Seen: {self.__last_seen}'
    
    def __eq__(self, other: 'Device') -> bool:
        """Verifica se os dispositivos são iguais com base nos hashes de seus endereços MAC"""
        if isinstance(other, Device):
            return self.mac_hash == other.mac_hash
        return False
