import os

# Nome da variável de ambiente que você deseja acessar
nome_variavel = "BUSID"

# Verifique se a variável de ambiente existe
if nome_variavel in os.environ:
    valor_variavel = os.environ[nome_variavel]
    print(f"Conteúdo da variável {nome_variavel}: {valor_variavel}")
else:
    print(f"A variável {nome_variavel} não está definida.")