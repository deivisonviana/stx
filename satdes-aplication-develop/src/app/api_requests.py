from config.api_config import API_URL_SATDES

import pandas as pd
import requests
from requests.exceptions import RequestException


def get_stations(filter: int) -> pd.DataFrame:
    """Obtém a lista de estações de acordo com o filtro especificado.

    Args:
        filter (int): O id do instituto para buscar as estações.

    Returns:
        pd.DataFrame: Um DataFrame contendo informações das estações.
    """
    try:
        # Requisitar ao backend a lista de todas de um determinado instituto
        response = requests.get(f'{API_URL_SATDES}/stations?filter[institute]={filter}', verify=False)
        response.raise_for_status()

        # Extrair a lista de estações da resposta JSON
        return pd.DataFrame(response.json()['data'])

    except RequestException as e:
        print(f"Erro ao obter a lista de estações: {e}")
    

def get_readed_files(ema: str) -> pd.DataFrame:
    """Obtém a lista de arquivos lidos de acordo com a estação EMA.

    Args:
        ema (str): Nome da estação EMA.

    Returns:
        pd.DataFrame: Um DataFrame contendo informações dos arquivos lidos.
    """
    # Definindo colunas do DataFrame, para caso a resposta seja vazia
    columns = ['id', 'name', 'file', 'date_make', 'date_read']

    try:
        # Requisita ao backend, a lista arquivos lidos de uma estação
        response = requests.get(f'{API_URL_SATDES}/readed/stations?filter[stations.name]={ema}', verify=False)
        response.raise_for_status()

        return pd.DataFrame(response.json()['data'], columns=columns)

    except RequestException as e:
        print(f"Erro: {e}")
