from datetime import datetime


def extract_probe_request_frame(probe_request_frame) -> [str, datetime]:
    """Extrai o MAC e a datetime do probe request e retorna um array [MAC, datetime]"""
    if not probe_request_frame.strip():
        return None
    
    device_info = []
    try:
        mac = probe_request_frame.split(' SA:')[1][0:17]
        if len(mac) != 17:
            raise ValueError
        device_info.append(mac)
        device_info.append(datetime.strptime(probe_request_frame[0:19], '%Y-%m-%d %H:%M:%S'))
    except (ValueError, IndexError):
        pass
    else:
        return device_info
