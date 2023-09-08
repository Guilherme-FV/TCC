from datetime import datetime
from datetime import timedelta
from src.device import Device

def test_device_creation():
    """Testando a criação de um objeto Device"""
    mac = "00:11:22:33:44:55"
    first_seen = datetime.now()
    device = Device(mac, first_seen)

    assert device is not None
    assert device.mac_hash is not None
    assert device.first_seen == first_seen
    assert device.last_seen == first_seen

def test_device_timeout():
    """Testando o método timeout"""
    mac = "00:11:22:33:44:55"
    first_seen = datetime.now()
    device = Device(mac, first_seen)

    assert not device.timeout()

    # Defina o last_seen para um tempo no passado para simular expiração
    device.last_seen = first_seen - timedelta(seconds=Device.TIMEOUT_SECONDS + 1)

    # O dispositivo deve estar expirado agora
    assert device.timeout()

def test_device_equality():
    """Testando a igualdade entre dispositivos"""
    mac1 = "00:11:22:33:44:55"
    mac2 = "66:77:88:99:AA:BB"
    first_seen1 = datetime.now()
    first_seen2 = first_seen1 + timedelta(seconds=10)

    device1 = Device(mac1, first_seen1)
    device2 = Device(mac2, first_seen2)
    device3 = Device(mac1, first_seen2)

    assert device1 == device1
    assert device1 == device3
    assert device1 != device2
