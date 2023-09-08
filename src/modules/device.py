from datetime import datetime
import hashlib


class Device:
    """Classe para criar dispositvos detecdados"""

    # Quantidade de segundos necessários para que um dispositivo seja considerado fora do ônibus
    TIMEOUT_SECONDS = 300
    
    def __init__(self, mac, first_seen):
        """Cria um objeto a partir do endereço MAC do dispositivo e da primeira vez que o dispositivo foi detectado em uma varredura"""
        # Usando SHA256 para anonimizar o endereço MAC
        self.__mac_hash = hashlib.sha256(mac.encode('utf-8')).hexdigest()
        self.__first_seen = first_seen
        self.__last_seen = first_seen


    def timeout(self) -> bool:
        """Verifica se o dispositivo está fora do ônibus"""
        if(datetime.now() - self.last_seen).total_seconds() > Device.TIMEOUT_SECONDS:
            return True
        return False
    
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
    
    def __str__(self) -> str:
        """Retorna uma representação em string do objeto"""
        return f'MAC_HASH: {self.__mac_hash} | First Seen: {self.__first_seen} | Last Seen: {self.__last_seen}'
    
    def __eq__(self, other: 'Device') -> bool:
        """Verifica se os dispositivos são iguais com base nos hashes de seus endereços MAC"""
        if isinstance(other, Device):
            return self.__mac_hash == other.__mac_hash
        return False
