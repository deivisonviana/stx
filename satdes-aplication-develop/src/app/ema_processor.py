import os
import pandas as pd

from app.api_requests import get_readed_files
from config.app_config import SFTP_DIR
from config.env_vars import ENV_VARS_SATDES, get_params
from utils.conn import connect_sftp, download_file, identify_missing_files, upload_files
from utils.json import create_temp_json


def process_ema_directory(connection, ema, station_data: pd.DataFrame) -> None:
    """Processa uma pasta de estação EMA no servidor FTP.

    Args:
        ftp (FTP): Objeto de conexão FTP.
        ema (str): Nome da estação EMA a ser processada.
        station_data (pd.DataFrame): DataFrame contendo informações das estações.

    Returns:
        None
    """
    # Criando conexão com SFTP Satdes
    sftp_satdes = connect_sftp(get_params(ENV_VARS_SATDES))

    # Procura o código da estação no sistema baseado no seu nome na origem
    station_row = (station_data.loc[station_data['name'] == ema]).squeeze()
    
    # Obtem os arquivos ja cadastrados/lidosp pro uma estação
    readed_files = get_readed_files(station_row['code'])

    # Consulta o banco de dados e identifica os arquivos não cadastrados
    missing_files = identify_missing_files(connection, ema, readed_files) 

    # Percorre cada arquivo que não está no "banco"
    for file in missing_files:
        if file.endswith(('.txt', '.proc')):
            # Baixa o arquivo do FTP de origem em formato CSV para um pd.Series
            df_station = download_file(connection, file)

            # Cria um arquivo JSON temporario para armazenar os dados baixados
            temp_file_path = create_temp_json(df_station)

            # Cria o path para transferência do arquivo
            remote_path = f"{SFTP_DIR}/{station_row['name_institute']}/{station_row['code']}/{os.path.splitext(file)[0]}.json"

            # Envia o arquivo para o SFTP do SATDES como JSON
            upload_files(sftp_satdes, temp_file_path, remote_path)

    # Fechando a conexão
    sftp_satdes.close()


def process_ema_insert():
    pass