from datetime import datetime
from src.modules.device import Device
from csv import reader
import src.modules.log_handler as log_handler
import pytest, os

DEVICES_AFTER_TIMEOUT_LOG_TEST = os.path.join('tests', 'logs', 'devices_after_timeout_test.csv')


@pytest.fixture
def probe_request_frame() -> str:
    """Retorna uma string simulando um probe request capturado pelo tcpdump"""
    return '2018-11-20 05:11:34.259737 10702424795us B 2437 MHz -76dBm signal BSSID:Broadcast DA:Broadcast SA:f4:f5:24:26:ba:4d (oui Unknown) Probe Request () [1.0 2.0 5.5 11.0 Mbit]'

@pytest.fixture
def device_list() -> [Device]:
    """Cria uma instância de Device para uso em testes"""
    devices = []

    for i in range(0, 4):
        mac = (str(i) + str(i) + ':' + str(i+1) + str(i+1) + ':' + str(i+2) + str(i+2) + ':' +
                str(i+3) + str(i+3) + ':' + str(i+4) + str(i+4) + ':' + str(i+5) + str(i+5))
        first_seen = datetime.now()
        devices.append(Device(mac, first_seen))
    
    return devices

def test_extract_probe_request_frame(probe_request_frame):
    """Verifica se a função está extraindo corretamente o timestamp e o MAC do probe request"""
    extracted_probe_request = log_handler.extract_probe_request_frame(probe_request_frame)

    assert extracted_probe_request[0] == 'f4:f5:24:26:ba:4d'
    assert extracted_probe_request[1] == datetime.strptime('2018-11-20 05:11:34', '%Y-%m-%d %H:%M:%S')

def test_save_devices_after_timeout(device_list):
    """Verifica se a função está salvando um dispositivo fora do ônibus no arquivo de log corretamente"""
    if os.path.exists(DEVICES_AFTER_TIMEOUT_LOG_TEST):
        os.remove(DEVICES_AFTER_TIMEOUT_LOG_TEST)

    log_handler.save_devices_after_timeout(device_list, DEVICES_AFTER_TIMEOUT_LOG_TEST)
    with open(DEVICES_AFTER_TIMEOUT_LOG_TEST, mode='r') as timeout_log:
        for index, line in enumerate(reader(timeout_log)):
            match index:
                case 1:
                    assert line == device_list[0].device_to_csv().split(',')
                case 2:
                    assert line == device_list[1].device_to_csv().split(',')
                case 3:
                    assert line == device_list[2].device_to_csv().split(',')
                case 4:
                    assert line == device_list[3].device_to_csv().split(',')
                case _:
                    continue