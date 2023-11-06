import pandas as pd
import requests
import json
import pyeto
from datetime import datetime, timedelta
import pytz
from collections import defaultdict
from statistics import mean
import os
from dotenv import load_dotenv

#carrega a variavel .env
load_dotenv()

# Constantes
TOKEN = os.getenv('token')
URL = os.getenv('url')
URL_ST = os.getenv('url_st')


def converter_horas(valor):
    horas = int(valor[:2]) if len(valor) >= 2 else 0
    minutos = int(valor[2:]) if len(valor) >= 4 else 0
    return f"{horas:02d}:{minutos:02d}"

def convert_to_datetime(time_str):
    # Converte de string para datatime
    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H%M")
    
    # Converte de UTC para hora local
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

import requests
import pandas as pd
from datetime import datetime, timedelta

# Função para obtenção de dados inmet no formato pandas
def sync_converter_router(data_inicial, data_final, cod_estacoes):
    # Inicializa uma lista vazia para armazenar os DataFrames
    dfs = []

    # Converte a data final em um objeto datetime e acrescenta um dia
    data_final = datetime.strptime(data_final, '%Y-%m-%d')
    data_final = data_final + timedelta(days=1)
    data_final = data_final.strftime("%Y-%m-%d")

    # Itera sobre as estações especificadas
    for estacao in cod_estacoes:
        # Constrói a URL da API com os parâmetros fornecidos
        url = URL + f'{data_inicial}/{data_final}/{estacao}/{TOKEN}'
        
        # Faz uma solicitação à API
        response = requests.get(url)

        if response.status_code == 200:
            try:
                # Analisa a resposta JSON
                data = response.json()

                # Processa os dados obtidos da API
                for item in data:
                    # Combina as informações de data e hora em um único campo
                    item['Data_Hora_UTC'] = item['DT_MEDICAO'] + ' ' + item['HR_MEDICAO']
                    # Converte a combinação em um objeto datetime
                    item['Data_Hora_UTC'] = convert_to_datetime(item['Data_Hora_UTC'])
                    # Adiciona um ID baseado na posição na lista
                    item['ID'] = data.index(item)
                    # Converte a data e hora em strings
                    item['DT_MEDICAO'] = str(item['Data_Hora_UTC'].date())
                    item['HR_MEDICAO'] = str(item['Data_Hora_UTC'].time())
                
                # Remove os primeiros 3 e os últimos 21 registros (ajuste personalizado)
                data = data[3:-21]
                
                # Se ainda houver dados, cria um DataFrame e o adiciona à lista
                if data:
                    df_station = pd.DataFrame(data)
                    dfs.append(df_station)
            except ValueError as e:
                print(f"Erro na decodificação JSON para a estação {estacao}: {e}")
        else:
            print(f"Solicitação para a estação {estacao} falhou com código de status: {response.status_code}")
    
    # Verifica se algum dado foi recuperado
    if not dfs:
        print("Nenhum dado foi recuperado para nenhuma estação.")
        return None

    # Concatena todos os DataFrames em um único DataFrame
    df = pd.concat(dfs, ignore_index=True)
    
    # Converte os objetos Timestamp em strings
    df['Data_Hora_UTC'] = df['Data_Hora_UTC'].astype(str)
    
    # Converte o DataFrame em um dicionário JSON
    json_result = df.to_dict(orient='records')
    
    # Retorna o resultado no formato JSON
    return json.dumps(json_result)

# Função para obtenção de dados inmet no formato json
def get_dados(data_inicial, data_final, estacao):
    url = f'{URL}{data_inicial}/{data_final}/{estacao}/{TOKEN}'
    response = requests.get(url)
    processed_data = []  # Define uma lista para armazenar os dados processados

    if response.status_code == 200:
        try:
            data = response.json()
            for item in data:
                item['Data_Hora_UTC'] = item['DT_MEDICAO'] + ' ' + item['HR_MEDICAO']
                item['Data_Hora_UTC'] = convert_to_datetime(item['Data_Hora_UTC'])
                item['ID'] = data.index(item)
                item['DT_MEDICAO'] = str(item['Data_Hora_UTC'].date())
                item['HR_MEDICAO'] = str(item['Data_Hora_UTC'].time())
            
            data = data[3:-21]  # Aplica o corte na lista, se necessário

            if data:
                processed_data.extend(data)  # Anexa os dados processados à lista
        except ValueError as e:
            print(f"JSON decoding error for station {estacao}: {e}")
    else:
        print(f"Request for station {estacao} failed with status code: {response.status_code}")

    if not processed_data:
        print(f"No data retrieved for station {estacao}.")

    # Converte objetos datetime em strings nos dados processados
    for item in processed_data:
        item['Data_Hora_UTC'] = str(item['Data_Hora_UTC'])

    # Converte o resultado final para o formato JSON
    if processed_data:
        json_result = json.dumps(processed_data, default=str, ensure_ascii=False, indent=4)
        return json_result
    else:
        return None

def temperatura_hora(data_inicial, data_final, estacao):
    # Recupere os dados usando a função get_dados
    json_data = get_dados(data_inicial, data_final, estacao)

    if json_data:
        try:
            # Analise os dados JSON em uma lista de dicionários
            data_list = json.loads(json_data)

            # Crie uma lista para armazenar as entradas de dados de temperatura
            hourly_data = []

            # Percorra os dados recuperados
            for entry in data_list:
                # Extraia e armazene os valores de temperatura
                hourly_entry = {
                    "DT_MEDICAO": entry['DT_MEDICAO'],
                    "HR_MEDICAO": entry['HR_MEDICAO'],
                    "TEM_MIN": entry['TEM_MIN'],
                    "TEM_MAX": entry['TEM_MAX'],
                }
                hourly_data.append(hourly_entry)

            # Retorne os dados em formato JSON
            json_result = json.dumps(hourly_data, ensure_ascii=False, indent=4)
            return json_result
        except json.JSONDecodeError as e:
            print(f"Erro na decodificação JSON: {e}")
            return None
    else:
        print("Nenhum dado recuperado.")
        return None


def temperatura_dia(data_inicial, data_final, estacao):
    # Recupera dados usando a função get_dados
    json_data = get_dados(data_inicial, data_final, estacao)

    if json_data:
        try:
            # Analisa os dados JSON em uma lista de dicionários
            data_list = json.loads(json_data)

            # Cria um dicionário para armazenar os dados diários de temperatura
            daily_data = defaultdict(lambda: {'DT_MEDICAO': None, 'TEM_MIN': [], 'TEM_MAX': [], 'TEM_INS': []})

            # Percorre os dados recuperados
            for entry in data_list:
                date_str = entry['DT_MEDICAO']  # 'DT_MEDICAO' contem a data
                date = daily_data[date_str]

                # Extrai e armazena os valores de temperatura
                date['DT_MEDICAO'] = date_str
                if entry['TEM_MIN'] is not None:
                    date['TEM_MIN'].append(float(entry['TEM_MIN']))
                if entry['TEM_MAX'] is not None:
                    date['TEM_MAX'].append(float(entry['TEM_MAX']))
                if entry['TEM_INS'] is not None:
                    date['TEM_INS'].append(float(entry['TEM_INS']))

            # Calcula as médias diárias
            daily_averages = list(daily_data.values())
            for entry in daily_averages:
                entry['TEM_MIN'] = round(mean(entry['TEM_MIN']), 1)
                entry['TEM_MAX'] = round(mean(entry['TEM_MAX']), 1)
                entry['TEM_INS'] = round(mean(entry['TEM_INS']), 1)

            # Retorna as médias diárias em formato JSON
            json_result = json.dumps(daily_averages, default=str, ensure_ascii=False, indent=4)
            return json_result
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None
    else:
        print("No data retrieved.")
        return None


def umidade_hora(data_inicial, data_final, estacao):
    # Recupere os dados usando a função get_dados
    json_data = get_dados(data_inicial, data_final, estacao)

    if json_data:
        try:
            # Analise os dados JSON em uma lista de dicionários
            data_list = json.loads(json_data)

            # Crie uma lista para armazenar as entradas de dados de umidade
            hourly_data = []

            # Percorra os dados recuperados
            for entry in data_list:
                # Extraia e armazene os valores de umidade
                hourly_entry = {
                    "DT_MEDICAO": entry['DT_MEDICAO'],
                    "HR_MEDICAO": entry['HR_MEDICAO'],
                    "UMD_MIN": entry['UMD_MIN'],
                    "UMD_MAX": entry['UMD_MAX'],
                }
                hourly_data.append(hourly_entry)

            # Retorne os dados em formato JSON
            json_result = json.dumps(hourly_data, ensure_ascii=False, indent=4)
            return json_result
        except json.JSONDecodeError as e:
            print(f"Erro na decodificação JSON: {e}")
            return None
    else:
        print("Nenhum dado recuperado.")
        return None


def umidade_dia(data_inicial, data_final, estacao):
    # Recupere os dados usando a função get_dados
    json_data = get_dados(data_inicial, data_final, estacao)

    if json_data:
        try:
            # Analise os dados JSON em uma lista de dicionários
            data_list = json.loads(json_data)

            # Crie uma lista para armazenar as entradas de dados de umidade
            daily_data = defaultdict(lambda: {'DT_MEDICAO': None, 'UMD_MIN': [], 'UMD_MAX': [], 'UMD_INS': []})

            # Percorra os dados recuperados
            for entry in data_list:
                date_str = entry['DT_MEDICAO']  # 'DT_MEDICAO' contem a data
                date = daily_data[date_str]

                # Extraia e armazene os valores de umidade
                date['DT_MEDICAO'] = date_str
                if entry['UMD_MIN'] is not None:
                    date['UMD_MIN'].append(float(entry['UMD_MIN']))
                if entry['UMD_MAX'] is not None:
                    date['UMD_MAX'].append(float(entry['UMD_MAX']))
                if entry['UMD_INS'] is not None:
                    date['UMD_INS'].append(float(entry['UMD_INS']))

            # Calcula as médias diárias
            daily_averages = list(daily_data.values())
            for entry in daily_averages:
                entry['UMD_MIN'] = round(mean(entry['UMD_MIN']), 1)
                entry['UMD_MAX'] = round(mean(entry['UMD_MAX']), 1)
                entry['UMD_INS'] = round(mean(entry['UMD_INS']), 1)

            # Retorne os dados em formato JSON
            json_result = json.dumps(daily_averages, default=str, ensure_ascii=False, indent=4)
            return json_result
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None
    else:
        print("No data retrieved.")
        return None


def precipitacao(data_inicial, data_final, estacao):
    # Recupere os dados usando a função get_dados
    json_data = get_dados(data_inicial, data_final, estacao)
    if json_data:
        try:
            # Analise os dados JSON em uma lista de dicionários
            data_list = json.loads(json_data)

            # Crie uma lista para armazenar as entradas de dados de chuva
            daily_data = defaultdict(lambda: {'DT_MEDICAO': None, 'CHUVA': []})

            # Percorra os dados recuperados
            for entry in data_list:
                date_str = entry['DT_MEDICAO']  # 'DT_MEDICAO' contem a data
                date = daily_data[date_str]

                # Extraia e armazene os valores de chuva
                date['DT_MEDICAO'] = date_str
                if entry['CHUVA'] is not None:
                    date['CHUVA'].append(float(entry['CHUVA']))
            # Calcula as médias diárias
            daily_averages = list(daily_data.values())
            for entry in daily_averages:
                entry['CHUVA'] = round(sum(entry['CHUVA']), 1)
            # Retorne os dados em formato JSON
            json_result = json.dumps(daily_averages, default=str, ensure_ascii=False, indent=4)
            return json_result
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None
    else:
        print("No data retrieved.")
        return None

# Defina um dicionário de mapeamento de cores para faixas de velocidade de vento
colors = {
    (0, 1): 'blue',
    (1, 3): 'green',
    (3, 5): 'yellow',
    (5, 7): 'orange',
    (7, float('inf')): 'red'
}

def get_color(velocity):
    try:
        velocity = float(velocity)  # Converte a velocidade para número
    except (ValueError, TypeError):
        return None  # Lidar com valores não numéricos ou nulos
    for (min_range, max_range), color in colors.items():
        if min_range <= velocity < max_range:
            return color

def vento(data_inicial, data_final, estacao):
    # Recupere os dados usando a função get_dados
    json_data = get_dados(data_inicial, data_final, estacao)
    
    if json_data:
        try:
            # Analise os dados JSON em uma lista de dicionários
            data_list = json.loads(json_data)
            
            # Defina uma lista para armazenar os dados filtrados
            filtered_data = []
        
            # Percorra os dados recuperados
            for entry in data_list:
                # Extraia campos relevantes e formate o horário
                hora_str = entry['HR_MEDICAO']  # Supondo que 'HR_MEDICAO' contenha a hora
                velocity = entry['VEN_VEL']
                color = get_color(velocity)  # Obtenha a cor com base na velocidade do vento
                if color is not None:  # Verifique se a cor não é nula
                    filtered_entry = {
                        'DT_MEDICAO': entry['DT_MEDICAO'],
                        'VEN_DIR': entry['VEN_DIR'],
                        'VEN_VEL': velocity,
                        'HORA': hora_str,
                        'COR': color  # Adicione a cor à saída
                    }
                    filtered_data.append(filtered_entry)
        
            # Retorne os dados filtrados como JSON
            json_result = json.dumps(filtered_data, default=str, ensure_ascii=False, indent=4)
            return json_result
        except json.JSONDecodeError as e:
            print(f"Erro na decodificação JSON: {e}")
            return None
    else:
        print("Nenhum dado recuperado.")
        return None


def evapo(data_inicial, data_final, estacao):
    # Supondo que a função 'get_dados' recupere os dados como uma string JSON
    json_data = get_dados(data_inicial, data_final, estacao)

    if json_data:
        try:
            # Analise os dados JSON em uma lista de dicionários
            data_list = json.loads(json_data)

            # Crie um dicionário para armazenar os dados diários de clima
            daily_data = defaultdict(lambda: {'DT_MEDICAO': None, 'TEM_MIN': [], 'TEM_MAX': [], 'TEM_INS': [], 'CHUVA': [], 'VL_LATITUDE': []})

            # Percorra os dados recuperados
            for entry in data_list:
                date_str = entry.get('DT_MEDICAO')  # Supondo que 'DT_MEDICACAO' contenha a data
                if date_str is not None:
                    date = daily_data[date_str]

                    # Extraia e armazene os valores de clima
                    date['DT_MEDICAO'] = date_str
                    if entry['TEM_MIN'] is not None:
                        date['TEM_MIN'].append(float(entry.get('TEM_MIN', 0)))
                    if entry['TEM_MAX'] is not None:
                        date['TEM_MAX'].append(float(entry.get('TEM_MAX', 0)))
                    if entry['TEM_INS'] is not None:
                        date['TEM_INS'].append(float(entry.get('TEM_INS', 0)))
                    if entry['CHUVA'] is not None:
                        date['CHUVA'].append(float(entry.get('CHUVA', 0)))
                    if entry['VL_LATITUDE'] is not None:
                        date['VL_LATITUDE'].append(float(entry.get('VL_LATITUDE', 0)))

            # Calcule as médias diárias
            daily_averages = list(daily_data.values())
            for entry in daily_averages:
                entry['TEM_MIN'] = round(min(entry['TEM_MIN']), 1)
                entry['TEM_MAX'] = round(max(entry['TEM_MAX']), 1)
                entry['TEM_INS'] = round(mean(entry['TEM_INS']), 1)
                entry['CHUVA'] = round(sum(entry['CHUVA']), 1)
                entry['VL_LATITUDE'] = mean(entry['VL_LATITUDE'])

                # Calcule a ET para esta entrada e adicione-a ao dicionário
                day_of_year = datetime.strptime(entry['DT_MEDICAO'], '%Y-%m-%d').timetuple().tm_yday
                sol_dec = pyeto.sol_dec(day_of_year)
                latitude = pyeto.deg2rad(entry['VL_LATITUDE'])
                sha = pyeto.sunset_hour_angle(latitude, sol_dec)
                ird = pyeto.inv_rel_dist_earth_sun(day_of_year)
                et_rad = pyeto.et_rad(latitude, sol_dec, sha, ird)
                eto = pyeto.hargreaves(entry['TEM_MIN'], entry['TEM_MAX'], entry['TEM_INS'], et_rad)
                entry['ET'] = round(eto, 2)

            # Retorne as médias diárias como JSON
            json_result = json.dumps(daily_averages, default=str, ensure_ascii=False, indent=4)
            return json_result
        except json.JSONDecodeError as e:
            print(f"Erro na decodificação JSON: {e}")
            return None
    else:
        print("Nenhum dado recuperado.")
        return None


