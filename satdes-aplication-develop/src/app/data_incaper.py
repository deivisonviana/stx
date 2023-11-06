import urllib3
from app.api_requests import get_stations
from app.ema_processor import process_ema_directory
from config.env_vars import ENV_VARS_INCAPER, get_params
from utils.conn import connect_sftp

# Desabilitar avisos do urllib3
urllib3.disable_warnings()

# Diretórios de estações EMA
EMAS = [
    'BJNORTE',
    'CACHOEIRO',
    'D_MARTINS',
    'IBITIRAMA',
    'IUNA',
    'MARILANDIA',
    'MUCURI',
    'PINHEIROS',
    'SORETAMA'
]

def job_incaper() -> None:
    """Executa o trabalho principal de busca, download e upload de arquivos
       entre servidores FTP e SFTP.

    Args:
        ftp (FTP): Objeto de conexão FTP com o servidor de origem.

    Returns:
        None
    """
    sftp = connect_sftp(get_params(ENV_VARS_INCAPER))

    # Obtem a lista de estações cadastradas no SATDES
    station_data = get_stations(filter=1)

    # Para cada pasta de estação
    for ema in EMAS:
        # Trocar para a pasta
        sftp.cwd(f"/henrique.dalmagro/{ema}")

        # Inicia o processo de transferencia da pasta
        process_ema_directory(sftp, ema, station_data) 

    # Fechando conexão
    sftp.close()


if __name__ == "__main__": 
    job_incaper()