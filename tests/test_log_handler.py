from datetime import datetime
import threading
from src.modules.device import Device
from csv import reader
import src.modules.log_handler as log_handler
import pytest, os, subprocess

DEVICES_AFTER_TIMEOUT_LOG_TEST = os.path.join('tests', 'logs', 'devices_after_timeout_test.csv')
TCPDUMP_LOG_TEST = os.path.join('tests', 'logs', 'tcpdump_test.txt')

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

def test_tcpdump_start():
    """Verifica se a função tcpdump_start está iniciando o processo do tcpdump conforme esperado"""
    tcp_process = log_handler.tcpdump_start(TCPDUMP_LOG_TEST)
    assert tcp_process.poll() is None
    tcp_process.terminate()
    tcp_process.wait()

    assert os.path.exists(TCPDUMP_LOG_TEST)
    assert os.path.getsize(TCPDUMP_LOG_TEST) > 0
    os.remove(TCPDUMP_LOG_TEST)

def test_tcpdump_stop():
    """Verfica se a função tcpdump_stop está finalizando o processo do tcpdump conforme esperado"""
    tcp_process = subprocess.Popen(["echo", "Fake tcpdump process"])
    log_handler.tcpdump_stop(tcp_process, TCPDUMP_LOG_TEST)
    
    timestr = datetime.time.strftime('%Y-%m-%d_%H-%M')
    expected_filename = f'Capture_{timestr}.txt'
    expected_path = os.path.join(os.path.dirname(TCPDUMP_LOG_TEST), 'dump', expected_filename)

    assert os.path.exists(expected_path)
    os.remove(expected_path)

def test_follow():
    follow_file = open(TCPDUMP_LOG_TEST, 'r')
    threading.Thread(target=log_handler.follow)
    loglines = log_handler.follow(follow_file)
    threading.Thread(target=write_follow_file)
    for line in loglines:
        assert line == "LINHA 1"

def write_follow_file():
    with open(TCPDUMP_LOG_TEST, 'w') as follow_file:
        follow_file.write("LINHA 1")
        follow_file.close()
        