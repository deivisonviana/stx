"""
Arquivo contendo o nome das chaves ENV referentes as conexão FTP e SFTP,
Citando desta maneira
"""

import os


ENV_VARS_INCAPER = {
    'host': "HOST_INCAPER",
    'user': "USER_INCAPER",
    'pass': "PASS_INCAPER",
    'port': "PORT_INCAPER"
}

ENV_VARS_CEPDEC = {
    'host': "HOST_CEPDEC",
    'user': "USER_CEPDEC",
    'pass': "PASS_CEPDEC",
    'port': "PORT_CEPDEC"
}

ENV_VARS_SATDES = {
    'host': "HOST_SATDES",
    'user': "USER_SATDES",
    'pass': "PASS_SATDES",
    'port': "PORT_SATDES"
}


def get_params(env_vars: dict):
    """
    Obtém parâmetros de conexão a partir de variáveis de ambiente.

    Args:
        env_vars (dict): Um dicionário que mapeia nomes de parâmetros aos nomes de variáveis de ambiente.

    Returns:
        dict or None: Um dicionário contendo os parâmetros de conexão obtidos das variáveis de ambiente,
                      ou None se alguma variável de ambiente não estiver definida.
    """
    # Inicializa um dicionário para armazenar os parâmetros de conexão
    params = dict()

    # Para cada chave (nome do parâmetro) na lista de variáveis de ambiente esperadas
    for key in env_vars:
        # Obtém o valor associado à variável de ambiente correspondente e o armazena no dicionário 'params'
        params[key] = os.environ.get(env_vars[key])

    # Verifica se algum dos valores dos parâmetros é None, o que indica que uma variável de ambiente não está definida
    if not all(params.values()):
        print("Erro! Alguma(s) variável(is) de ambiente não foi(ram) definida(s).")
        return None  # Retorna None se alguma variável de ambiente não estiver definida

    # Retorna o dicionário de parâmetros de conexão obtidos com sucesso
    return params  
