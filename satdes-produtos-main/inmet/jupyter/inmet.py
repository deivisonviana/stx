import api_file
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import pytz

# Contantes
TOKEN = api_file.token
URL = 'https://apitempo.inmet.gov.br/token/estacao/'
URL_ST = 'https://apitempo.inmet.gov.br/estacoes/'

def converter_horas(valor):
    horas = int(valor[:2]) if len(valor) >= 2 else 0
    minutos = int(valor[2:]) if len(valor) >= 4 else 0
    return f"{horas:02d}:{minutos:02d}"

def convert_to_datetime(time_str):
    # Parse the time string into a datetime object
    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H%M")
    
    # Create a timezone object (e.g., UTC)
    desired_timezone = pytz.timezone('America/Sao_Paulo')
    data_hora_local = time_obj.astimezone(desired_timezone)
    data_hora_local_sem_fuso = data_hora_local.replace(tzinfo=None)
    data_hora_local_sem_fuso = data_hora_local_sem_fuso - timedelta(hours=3)
    
    return data_hora_local_sem_fuso

# Função para recuperar todas as estações de acordo com o tipo (automáticas ou manuais)
def get_estacoes(tipo='B'):
    url = URL_ST + tipo

    def request_data(tipo):
        response = requests.get(url, timeout=120.0)
        
        return json.loads(response.text)

    # Baixa os dados das estações automaticas e manuais
    if tipo == "B":
        responseM = request_data("M")
        responseT = request_data("T")

        # Concatena as duas respostas em um unico dataframe
        data = pd.concat([pd.DataFrame(responseM), pd.DataFrame(responseT)])

    else:
        response = request_data(tipo)
        data = pd.DataFrame(response)
        
    return data

def sync_converter_router(data_inicial, data_final, cod_estacoes):
    dfs = []
    data_final = datetime.strptime(data_final, '%Y-%m-%d')
    data_final = data_final + timedelta(days=1)
    data_final = data_final.strftime("%Y-%m-%d")
    
    for estacao in cod_estacoes:
        url = URL + f'{data_inicial}/{data_final}/{estacao}/{TOKEN}'
        response = requests.get(url)

        if response.status_code == 200:  # Check if the request was successful
            try:
                data = response.json()
                df = pd.DataFrame(data)
                df['Data_Hora_UTC'] = df['DT_MEDICAO'] + ' ' + df['HR_MEDICAO']
                df['Data_Hora_UTC'] = df['Data_Hora_UTC'].apply(convert_to_datetime)
                df['ID'] = df.index
                df['DT_MEDICAO'] = df['Data_Hora_UTC'].dt.date
                df['HR_MEDICAO'] = df['Data_Hora_UTC'].dt.time
                df = df.iloc[3:]
                df = df.iloc[:-21]
                dfs.append(df)
            except ValueError as e:
                print(f"error for station {estacao}: {e}")
        else:
            print(f"Request for station {estacao} failed with status code: {response.status_code}")
    
    if not dfs:
        print("No data retrieved for any station.")
        return None

    df = pd.concat(dfs, ignore_index=True)
    return df



