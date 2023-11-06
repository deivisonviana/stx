import os
import pytz

# Configurações de PATH
DATA_DIR = os.environ.get("DATA_DIR") # Caminho para salvar os dados baixados
SFTP_DIR = os.environ.get("SFTP_DIR") # Caminnho para baixar os dados no servidor SFTP
LOGS_DIR = os.environ.get("LOGS_DIR") # Caminho para salvar os logs dos scripts

# Configuração de fuso-horario
TIME_ZONE = pytz.timezone('America/Sao_Paulo')
