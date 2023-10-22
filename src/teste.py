from os import devnull
import subprocess

# def tcpdump_start(arquivo_saida_param) -> subprocess.Popen:
#     """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
#     tcp_args = ['sudo', 'tcpdump', '-i', 'eth0', '-e', '-ttt', '-U']
#     return subprocess.Popen(tcp_args, stdout = open(arquivo_saida_param, 'w', encoding='utf-8'), stderr = open(devnull, 'w', encoding='utf-8'))


def tcpdump_start(arquivo_saida_param) -> subprocess.Popen:
    """Inicia o processo do tcpdump direcionando seu output para o arquivo de log"""
    tcp_args = ['tcpdump', '-i', 'wlan1', '-e', '-ttt', '-U', 'wlan[0]=0x80', 'or', 'wlan[0]=0x40', 'or', 'wlan[0]=0x50']
    with subprocess.Popen(tcp_args, stdout = open(arquivo_saida_param, 'w', encoding='utf-8'), stderr = open(devnull, 'w', encoding='utf-8')) as tcpdump_process:
        if tcpdump_process.poll() is None:
            print("O processo está em execução.")
        return tcpdump_process
# Nome do arquivo de saída
arquivo_saida = "saida.txt"

# Executar o comando com subprocess
processo = tcpdump_start(arquivo_saida)

# Aguardar até que o tcpdump termine de executar
saida, erro = processo.communicate()

# Verificar se houve erros
if erro:
    print(f"Erro ao executar tcpdump: {erro.decode('utf-8')}")
else:
    print(f"tcpdump executado com sucesso. Saída gravada em {arquivo_saida}")
