from datetime import datetime
import csv, os


DEVICES_AFTER_TIMEOUT_LOG = os.path.join('logs', 'devices_after_timeout.csv')

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

def save_devices_after_timeout(devices, path = DEVICES_AFTER_TIMEOUT_LOG):
    data = []
    for device in devices:
        data.append(device.device_to_csv().split(','))
    
    if not os.path.isfile(path):
        open_mode = 'w'
    else:
        open_mode = 'a'
    with open(path, mode=open_mode, newline='') as timeout_log:
        csv_writer = csv.writer(timeout_log)
        if open_mode == 'w':
            csv_writer.writerow(['mac_hash','fseen_date','fseen_time','lseen_date','lseen_time'])
        csv_writer.writerows(data)
