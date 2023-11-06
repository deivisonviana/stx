import os

# Configurações de API
API_URL_SATDES = os.environ.get("API_URL_SATDES")   # URL para requisição do banco de dados
API_URL_INMET = os.environ.get("API_URL_INMET") # URL base para utilizar a API
API_URL_ANA = os.environ.get("API_URL_ANA") # URL base da API da ANA

API_KEY_INMET = os.environ.get("API_KEY_INMET") # Token de acesso a API do INMET
