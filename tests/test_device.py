import pytest
from datetime import datetime, timedelta
from src.modules.device import Device

@pytest.fixture
def device_instance():
    """Cria uma instância de Device para uso em testes"""
    mac = "00:11:22:33:44:55"
    first_seen = datetime.now()
    return Device(mac, first_seen)

def test_timeout(device_instance):
    """Verifica se o timeout está funcionando corretamente quando um dispositivo não é visto por TIMEOUT_SECONDS segundos"""
    assert not device_instance.timeout()
    device_instance.last_seen = datetime.now() - timedelta(seconds=Device.TIMEOUT_SECONDS + 1)
    assert device_instance.timeout()

def test_equality(device_instance):
    """Verifica se a função de igualdade está funcionando corretamente ao comparar dispositivos"""
    other_device = Device("00:AA:BB:CC:DD:EE", datetime.now())
    assert device_instance == device_instance
    assert device_instance != other_device

def test_string_representation(device_instance):
    """Verifica se a representação em string está correta"""
    expected_str = f'MAC_HASH: {device_instance.mac_hash} | First Seen: {device_instance.first_seen} | Last Seen: {device_instance.last_seen}'
    assert str(device_instance) == expected_str
