"""
Esta função coordena o processo de transferência de arquivos de uma origem FTP para um destino SFTP
de acordo com as seguintes etapas:

1. Obtém a lista de estações cadastradas no sistema SATDES com base em um filtro específico.

2. Para cada pasta no servidor FTP de origem:
    - Troca para a pasta correspondente.
    - Lista as pastas (estações EMA) presentes nessa pasta.

3. Para cada pasta de estação EMA encontrada no servidor FTP:
    - Troca para a pasta da estação.
    - Inicia o processo de transferência da pasta utilizando a função process_ema_directory.
"""
import urllib3
from app.api_requests import get_stations
from app.ema_processor import process_ema_directory
from config.env_vars import ENV_VARS_CEPDEC, get_params

from utils.conn import connect_ftp

# Desabilitar avisos do urllib3
urllib3.disable_warnings()

# Diretórios de estações EMA
EMA_DIRS = [
    'EMA-Cepdec',
    'EMA-Parceiros'
]

def job_cepdec() -> None:
    """Executa o trabalho principal de busca, download e upload de arquivos
       entre servidores FTP e SFTP.

    Args:
        ftp (FTP): Objeto de conexão FTP com o servidor de origem.

    Returns:
        None
    """
    ftp = connect_ftp(get_params(ENV_VARS_CEPDEC))

    # Obtem a lista de estações cadastradas no SATDES
    station_data = get_stations(filter=2)

    # Para cada pasta no FTP
    for dir in EMA_DIRS:
        # Trocar o diretorio
        ftp.cwd(f"/{dir}")

        # Listar as pastas na pasta
        ema_dirs = ftp.nlst()

        # Para cada pasta de estação
        for ema in ema_dirs:
            # Trocar para a pasta
            ftp.cwd(f"/{dir}/{ema}")

            # Inicia o processo de transferencia da pasta
            process_ema_directory(ftp, ema, station_data) 

    # Fechando conexão
    ftp.close()


if __name__ == "__main__":
    job_cepdec()
