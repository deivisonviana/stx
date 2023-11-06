
import urllib3
from app.api_requests import get_stations

from config.env_vars import ENV_VARS_INCAPER, get_params
from utils.conn import connect_ftp


# Desabilitar avisos do urllib3
urllib3.disable_warnings()

# Diretórios de estações EMA
EMA_DIRS = [
    ...
]

def job_satdes() -> None:
    """Executa o trabalho principal de busca, download e upload de arquivos
       entre servidores FTP e SFTP.

    Args:
        ftp (FTP): Objeto de conexão FTP com o servidor de origem.

    Returns:
        None
    """
    sftp = connect_ftp(get_params(ENV_VARS_INCAPER))

    # Obtem a lista de estações cadastradas no SATDES
    station_data = get_stations(filter=3)

    # Para cada pasta no FTP
    for dir in EMA_DIRS:
        # Trocar o diretorio
        sftp.cwd(f"/{dir}")

        # Listar as pastas na pasta
        ema_dirs = sftp.listdir()

        # Para cada pasta de estação
        for ema in ema_dirs:
            # Trocar para a pasta
            sftp.cwd(f"/{dir}/{ema}")

            

if __name__ == "__main__":
    # Criando a conexão com FTP
    try:
        job_satdes()
            
    except Exception as e:
        print(f"Um erro inexperado ocrreu: {e}")

    