from os import devnull
import subprocess

from modules.log_handler import TCPDUMP_LOG

def tcpdump_start() -> subprocess.Popen:
    """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
    tcp_args = ['sudo', 'tcpdump', '-i', 'eth0', '-e', '-U']
    return subprocess.Popen(tcp_args, stdout = open(TCPDUMP_LOG, 'w', encoding='utf-8'), stderr = open(devnull, 'w', encoding='utf-8'))

# Executar o comando com subprocess
processo = tcpdump_start()

# Aguardar até que o tcpdump termine de executar
saida, erro = processo.communicate()

# Verificar se houve erros
if erro:
    print(f"Erro ao executar tcpdump: {erro.decode('utf-8')}")
else:
    print(f"tcpdump executado com sucesso. Saída gravada em {TCPDUMP_LOG}")
