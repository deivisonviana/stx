import logging
import requests
import pandas as pd

from config.api_config import API_URL_INMET, API_KEY_INMET
from config.app_config import TIME_ZONE

def get_data_times(date: str, hour: str) -> pd.DataFrame | None:
    """Obtém dados horários referentes a todas as estações automáticas de um dia

    Args:
        date (str): Data para consulta (formato "YYYY-MM-DD")
        hour (str): Horário da consulta (formato "HHMM")
        token (str): Token de acesso a API do INMET.

    Returns:
        pd.DataFrame | None: Retorna um DataFrame contendo as informações ou None em caso de erro.
    """
    try:
        response = requests.get(
            f"{API_URL_INMET}/estacao/dados/{date}/{hour}/{API_KEY_INMET}", timeout=10, verify=False
        )
        # Verifica se houve erro na requisição
        response.raise_for_status()

        df_es = pd.DataFrame(response.json())
        df_es = convert_utc_inmet(df_es)
        # Estações que não estão em uso
        df_es = df_es[~df_es['CD_ESTACAO'].isin(['A623', 'A650'])]

        logging.info(
            f"Dados requisitados com sucesso! - status: {response.status_code}"
        )

        return df_es

    except requests.exceptions.RequestException as error:
        logging.error(
            f"Erro na requisição - status: {response.status_code}\nerro: {error}"
        )

        return None
    
def get_data_manuals(current_date: str, previous_date: str) -> pd.DataFrame | None:
    """
    Obtém dados horários referentes a todas as estações manuais de 1 semana

    Args:
        current_date (str): Data atual (formato "YYYY-MM-DD")
        previous_date (str): Data anterior há uma semana (formato "YYYY-MM-DD")
    
    Returns:
        pd.DataFrame | None: Retorna um DataFrame contendo as informações ou None em caso de erro
    """
    try:
        code_stations = ['83013', '83648']
        dataframes = []

        for code_station in code_stations:
            response = requests.get(
                f"{API_URL_INMET}/estacao/{previous_date}/{current_date}/{int(code_station)}/{API_KEY_INMET}"
            )
            response.raise_for_status()

            df = pd.DataFrame(response.json())
            dataframes.append(df)

            logging.info(
                f"Dados requisitados com sucesso! - Status: {response.status_code}"
            )
        df_set = pd.concat(dataframes, ignore_index=True)
        df_set = convert_utc_inmet(df_set)

        return df_set
    
    except requests.exceptions.RequestException as error:
        logging.error(
            f"Erro na requisição - Status: {response.status_code}\nerro: {error}"
        )

        return None

def convert_utc_inmet(df_inmet: pd.DataFrame) -> pd.DataFrame:
    """
    Converte as informações de data e hora em um DataFrame do INMET (Instituto Nacional de Meteorologia)
    para o horário local do Espírito Santo (ES) e retorna o DataFrame resultante com timestamps Unix.

    Args:
        df_inmet (pd.DataFrame): Um DataFrame contendo os dados do INMET.

    Returns:
        pd.DataFrame: Um DataFrame com as informações de data e hora convertidas para o horário local do ES
                      e representadas como timestamps Unix (segundos desde 1970-01-01 00:00:00 UTC) como int32.
    """
    # Filtra as linhas onde a coluna "UF" começa com "ES" e define a coluna "INSTITUICAO" como "INMET"
    df_es = df_inmet[df_inmet["UF"].str.startswith("ES")].assign(INSTITUICAO="INMET")

    # Combina as colunas "DT_MEDICAO" e "HR_MEDICAO" em uma única coluna "DATA_HORA" no formato 'YYYY-MM-DD HHMM'
    df_es["DATA_HORA"] = df_es["DT_MEDICAO"] + " " + df_es["HR_MEDICAO"].str.zfill(4)

    # Converta 'DATA_HORA' para datetime
    df_es["DATA_HORA"] = pd.to_datetime(
        df_es["DATA_HORA"], format="%Y-%m-%d %H%M", utc=True
    )

    # Converte a coluna "DATA_HORA" para a hora local usando o fuso horário do ES (Espírito Santo)
    df_es["DATA_HORA"] = df_es["DATA_HORA"].dt.tz_convert(TIME_ZONE)

    # Converte a coluna "DATA_HORA" para timestamp Unix (segundos desde 1970-01-01 00:00:00 UTC) como int32
    df_es["DATA_HORA"] = pd.to_datetime(df_es["DATA_HORA"]).astype("int64") // 10**9
    df_es["DATA_HORA"] = df_es["DATA_HORA"].astype("int32")

    # Retorna o array com horario timestamp convertido
    return df_es

def split_dataframe_stations_inmet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um Dataframe do INMET com os dados de todas as estações e divide os dados para cada estação em um dataframe.

    Args:
        df (pd.DataFrame): Um dataframe com os dados de todas as estações

    Returns:
        pd.DataFrame: Um dataframe com dados de cada estação
    """
    dataframes = {}
    stations = df['CD_ESTACAO'].unique()

    for station in stations:
        dataframes[station] = df[df['CD_ESTACAO'] == station]

    return dataframes
