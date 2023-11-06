import os
import json
import logging
import tempfile
import requests
import urllib3
import pandas as pd

from config.env_vars import ENV_VARS_SATDES, get_params
from config.api_config import API_URL_SATDES
from config.app_config import DATA_DIR, SFTP_DIR
from utils.conn import connect_sftp

urllib3.disable_warnings()

def handle_exceptions(func: callable):
    """
    Um decorador que lida com exceções específicas durante a execução de uma função.

    Este decorador envolve a função passada como argumento em um bloco try-except e registra erros
    específicos que podem ocorrer durante a execução da função.

    Args:
        func (callable): A função que será decorada.

    Returns:
        callable: A função decorada.
    """
    def wrapper(*args, **kwargs):
        # Tenta executar a função passada como argumento
        try:
            return func(*args, **kwargs)

        except FileNotFoundError as fnf_error:
            # Registra um erro se um arquivo ou pasta não for encontrado
            logging.error(
                f"Erro: Pasta ou arquivo não encontrado - {fnf_error}")

        except json.JSONDecodeError as json_decode_error:
            # Registra um erro se houver um erro de decodificação JSON
            logging.error(f"Erro ao decodificar JSON: {json_decode_error}")

        except pd.errors.EmptyDataError as empty_data_error:
            # Registra um erro se um DataFrame estiver vazio
            logging.error(f"Erro: DataFrame vazio - {empty_data_error}")

        except Exception as error:
            # Registra um erro genérico se ocorrer qualquer outra exceção não tratada
            logging.error(f"Erro desconhecido: {error}")

    return wrapper


@handle_exceptions
def save_json(data: pd.DataFrame, file_name: str) -> None:
    """
    Salva um DataFrame em formato JSON.

    Args:
        data (DataFrame): Um DataFrame contendo os dados das estações.
        file_name (str): O nome do arquivo no qual os dados serão salvos.
    """
    # Converte o DataFrame para uma lista de dicionários
    data_dict = data.to_dict(orient="records")

    # Escreve o JSON no arquivo com a codificação UTF-8
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data_dict, file, ensure_ascii=False, indent=4)
    # Realiza o upload no servidor SFTP
    upload_sftp(file_name)
    # Remove o arquivo do diretório depois que foi realizado o upload no stfp
    os.remove(file_name)


@handle_exceptions
def upload_sftp(file_json: str) -> None:
    """
    Carrega um arquivo para uma pasta do servidor SFTP

    Args:
        file_json (str): Nome do arquivo gerado
    """
    # Pega a primeira parte do nome do arquivo
    institution = file_json.split('_')[0]

    # Pega o código da estação no nome do arquivo
    code = file_json.split('_')[1]

    # Estabelecendo conexão com o servidor SFTP
    with connect_sftp(get_params(ENV_VARS_SATDES)) as sftp:
        print("Conexão Estabelecida com sucesso!")
        # Estrutura condicional para jogar cada arquivo em sua determinada pasta do servidor por instituição
        if institution == "inmet":

            # Requisição a API para conferir se a estação existe e pegar seu código
            response = requests.get(f'{API_URL_SATDES}/stations?filter[institute]=3', verify=False)
            response.raise_for_status()
            data = pd.DataFrame(response.json()['data'])

            # Verificação da estação, nome e código
            for index, row in data.iterrows():
                name_station = row['name']
                if name_station == code:
                    code_station = row['code']
                    # Verifica se a pasta existe no SFTP
                    if not sftp.exists(SFTP_DIR + f"/INMET/{code_station}"):
                        sftp.mkdir(SFTP_DIR + f"/INMET/{code_station}")
                    # Vai para o diretório e faz o upload
                    sftp.cwd(SFTP_DIR + f"/INMET/{code_station}")
                    sftp.put(file_json)
                    print(
                        f"Arquivo {file_json} enviado com sucesso para a pasta {SFTP_DIR}/INMET/{code_station} do servidor")
            # Fecha a conexão
            sftp.close()

        elif institution == "ana":
            sftp.cwd(SFTP_DIR + "/ANA")

            sftp.put(file_json)
            sftp.close()
            print(
                f"Arquivo {file_json} enviado com sucesso para a pasta ANA do servidor")

        else:
            sftp.close()
            print(f"Instituição {institution} não está cadastrada no sistema")

@handle_exceptions
def load_json(file_path: str) -> list:
    """
    Carrega dados de um arquivo JSON a partir de um caminho especificado.

    Args:
        file_path (str): O caminho do arquivo JSON a ser carregado.

    Returns:
        list: Uma lista contendo os dados carregados do arquivo JSON.
    """
    # Cria o caminho completo para o arquivo
    dir = os.path.join(DATA_DIR, file_path)

    # Carrega o JSON do arquivo
    with open(dir, "r") as file_json:
        data = pd.read_json(file_json)

    # Retorna os dados carregados do arquivo JSON
    return data

def create_temp_json(data: pd.DataFrame):
    # Criar um arquivo temporário para armazenar o JSON
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as temp_file:
        # Converter o DataFrame para JSON
        json_data = data.to_json(orient='values')
        temp_file.write(json_data)
    
    return temp_file.name
