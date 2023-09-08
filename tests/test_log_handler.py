from datetime import datetime
import src.modules.log_handler as log_handler
import pytest


@pytest.fixture
def probe_request_frame() -> str:
    """Retorna uma string simulando um probe request capturado pelo tcpdump"""
    return '2018-11-20 05:11:34.259737 10702424795us B 2437 MHz -76dBm signal BSSID:Broadcast DA:Broadcast SA:f4:f5:24:26:ba:4d (oui Unknown) Probe Request () [1.0 2.0 5.5 11.0 Mbit]'

def test_extract_probe_request_frame(probe_request_frame):
    """Verifica se a função está extraindo corretamente o timestamp e o MAC do probe request"""
    extracted_probe_request = log_handler.extract_probe_request_frame(probe_request_frame)

    assert extracted_probe_request[0] == 'f4:f5:24:26:ba:4d'
    assert extracted_probe_request[1] == datetime.strptime('2018-11-20 05:11:34', '%Y-%m-%d %H:%M:%S')
