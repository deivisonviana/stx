import io
import pysftp
import ftplib
import pandas as pd
from typing import Union

def download_file(connection: Union[pysftp.Connection, ftplib.FTP], file: str):
    """Baixa um arquivo do servidor (FTP ou SFTP) e o carrega em um DataFrame.

    Args:
        connection: Objeto de conexão (pysftp.Connection ou FTP).
        file (str): Nome do arquivo a ser baixado.

    Returns:
        pd.DataFrame: O DataFrame com os dados do arquivo.
    """
    with io.BytesIO() as file_buffer:
        # Baixe o arquivo binário do servidor SFTP de origem
        if isinstance(connection, pysftp.Connection):
            connection.getfo(file, file_buffer)

        # Baixe o arquivo binário do servidor FTP de origem
        elif isinstance(connection, ftplib.FTP):
            connection.retrbinary(f'RETR {file}', file_buffer.write)
            
        else:
            raise ValueError("Tipo de conexão não suportado.")

        # Volte ao início do buffer
        file_buffer.seek(0)

        # Carregue os dados do arquivo em um DataFrame
        return pd.read_csv(file_buffer, sep=',', header=None).iloc[0]


def upload_files(connection: Union[pysftp.Connection, ftplib.FTP], tempt_path: str, remote_path: str) -> None:
    """Faz upload de um arquivo em formato JSON para um servidor FTP ou SFTP.

    Args:
        connection: Objeto de conexão (pysftp.Connection ou FTP).
        file_sr (pd.Series): A série de dados a ser carregada em JSON.
        path (str): O diretório de destino no servidor FTP ou SFTP.
        file_name (str): Nome do arquivo a ser criado.

    Returns:
        None
    """
    # Transferência para SFTP
    if isinstance(connection, pysftp.Connection):
        connection.put(tempt_path, remote_path)

    # Transferência para FTP
    elif isinstance(connection, ftplib.FTP):
        with open(tempt_path, 'rb') as local_file:
            connection.storbinary(f'STOR {remote_path}', local_file)
    else:
        raise ValueError("Tipo de conexão não suportado.")
    


def identify_missing_files(connection: Union[pysftp.Connection, ftplib.FTP], ema: str, readed_files: str) -> pd.Series:
    """Identifica os arquivos ausentes na estação EMA em um servidor FTP ou SFTP.

    Args:
        connection: Objeto de conexão (pysftp.Connection ou FTP).
        ema (str): Nome da estação EMA.

    Returns:
        pd.Series: Uma série de arquivos ausentes na estação EMA.
    """
    if isinstance(connection, pysftp.Connection):
         # Criar um dataframe com os arquivos da pasta
        ema_files = connection.listdir()

    elif isinstance(connection, ftplib.FTP): 
        ema_files = connection.nlst()
   
    ema_files = pd.Series(ema_files)

    # Comparar arquivos entre FTP/SFTP e DataFrame da API
    return ema_files[~ema_files.isin(readed_files['file'])]


def connect_sftp(params: dict) -> pysftp.Connection|None:
    """
    Função para conectar a um servidor SFTP de dados.

    Returns:
        pysftp.Connection: Um objeto de conexão com o servidor SFTP.
    """
    # Indicando ao ftp não buscar uma chave SSH
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    # Criando objeto de conexão
    try:
        sftp = pysftp.Connection(
            host=params["host"],
            username=params["user"],
            password=params["pass"],
            port=int(params["port"]),
            cnopts=cnopts,
        )
        # Retornando conexão
        return sftp

    except Exception as error:
        print(f"Erro ao conectar no SFTP: {error}")

        return None


def connect_ftp(params: dict) -> ftplib.FTP|None:
    """
    Função para conectar a um servidor FTP

    Returns:
        FTP|None: Um objeto de conexão com o servidor FTP
    """
    # Criando objeto de conexão
    try:
        ftp = ftplib.FTP(host=params["host"])
        ftp.login(
            user=params["user"], 
            passwd=params["pass"], 
            acct=""
        )
        # Retornando a conexão
        return ftp

    except Exception as error:
        print(f"Erro con conectar no FTP: {error}")

        return None
    