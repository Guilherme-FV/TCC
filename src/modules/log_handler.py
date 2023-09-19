from datetime import datetime
import csv, os, subprocess, shutil, time


DEVICES_AFTER_TIMEOUT_LOG = os.path.join('logs', 'devices_after_timeout.csv')
TCPDUMP_LOG = os.path.join('logs', 'tcpdump.txt')

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
    """Salva os dispositivos que não estão mais presentes na área no arquivo de log"""
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

def tcpdump_start(path = TCPDUMP_LOG) -> subprocess.Popen:
    """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
    with open(path, 'w') as tcpdump_log:
        tcp_args = ['tcpdump', '-i', 'wlan0mon', '-e', '-ttt', '-U', 'wlan[0]=0x80', 'or', 'wlan[0]=0x40', 'or', 'wlan[0]=0x50']
        tcp_process = subprocess.Popen(tcp_args, stdout = tcpdump_log, stderr = open(os.devnull, 'w'))
    return tcp_process

def tcpdump_stop(tcp_process, path = TCPDUMP_LOG):
    """Finaliza o processo tcpdump e salva o arquivo atual de captura"""
    tcp_process.send_signal(subprocess.signal.SIGTERM)
    tcp_process.communicate()

    timestr = time.strftime('%Y-%m-%d_%H-%M')
    dump_filename = f'Capture_{timestr}.txt'
    dump_full_path = os.path.join(os.path.dirname(path), 'dump', dump_filename)
    
    try:
        shutil.move(path, dump_full_path)
    except IOError:
        pass

def follow(log_file = TCPDUMP_LOG):
    """Função que captura inserções conforme alimentadas no log"""
    log_file.seek(0,2)
    while True:
        line = log_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
