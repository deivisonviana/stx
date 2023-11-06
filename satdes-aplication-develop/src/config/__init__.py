from dotenv import load_dotenv

load_dotenv()

from .api_config import API_URL_SATDES, API_URL_ANA, API_URL_INMET, API_KEY_INMET
from .app_config import DATA_DIR, LOGS_DIR, TIME_ZONE, SFTP_DIR
from .env_vars   import ENV_VARS_SATDES, ENV_VARS_INCAPER, ENV_VARS_CEPDEC, get_params