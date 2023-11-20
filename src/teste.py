import json

def escrever_em_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)


def ler_arquivo_json(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        mensagens = json.load(arquivo)[0]['messages']
        dados = []
        for mensagem in mensagens:
            if mensagem['topic'] == 'num_passengers':
                conteudo = json.loads(mensagem['payload'])
                info_mensagem = {
                    'topico': 'num_passengers',
                    'veiculo_id': conteudo['veiculo_id'],
                    'lotacao': conteudo['lotacao'],
                    'data': conteudo['data'],
                    'hora': conteudo['hora']
                }
                dados.append(info_mensagem)
                
            if mensagem['topic'] == 'exit_devices':
                conteudo = json.loads(mensagem['payload'])
                for device in conteudo:
                    json_device = json.loads(device)
                    print(json_device['posicao_entrada_latitude'])
                    info_mensagem = {
                        'topico': 'exit_devices',
                        'veiculo_id': json_device['veiculo_id'],
                        'mac_hash': json_device['mac_hash'],
                        'entrada': json_device['entrada'],
                        'saida': json_device['saida'],
                        'data_entrada': json_device['data_entrada'],
                        'data_saida': json_device['data_saida'],
                        'posicao_entrada_latitude': json_device['posicao_entrada_latitude'],
                        'posicao_entrada_longitude': json_device['posicao_entrada_longitude'],
                        'posicao_saida_latitude': json_device['posicao_saida_latitude'],
                        'posicao_saida_longitude': json_device['posicao_saida_longitude']
                    }
                    dados.append(info_mensagem)
        return dados

nome_do_arquivo = 'src/ModRecbTeste1.json'
dados_json = ler_arquivo_json(nome_do_arquivo)
escrever_em_json(dados_json, 'testeaaaaaaaaa.json')