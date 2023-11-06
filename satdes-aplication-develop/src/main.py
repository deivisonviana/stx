"""
Esta função executa as seguintes etapas:
1. Obtém a data atual.
2. Calcula o horário UTC atual usando a função get_utc_time().
3. Gera um nome de arquivo JSON usando a data e o horário.
4. Chama a função get_data_times() para obter os dados das estações automáticas do INMET.
5. Chama a função get_data_manuals() para obter os dados das estações manuais do INMET.
6. Chama a função get_data_ana() para obter os dados das estações de hora em hora da ANA.
7. Chama a função save_json() para salvar os dados em um arquivo JSON.
8. Imprime os dados obtidos.
"""
import datetime as dt
import logging
import schedule
import time

from app.data_processor import DataProcessor
from app.data_inmet import get_data_times, get_data_manuals, split_dataframe_stations_inmet
from app.data_ana import get_data_ana
from utils.time import get_utc_time
from utils.json import save_json

# Configurando o sistema de LOG
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

"""
    Variáveis Globais
        - date (str): Data atual (formato "YYYY-MM-DD")
        - previous_date (str): Data anterior há uma semana
        - formatted_date (str): Data atual, porém no formato DD/MM/YYYY
        - hour (str): Horário da consulta (formato "HHMM")
"""

# Obtém a data atual
date = dt.datetime.today().date()

# Data atual formatada para DD/MM/YYYY
formatted_date = date.strftime("%d/%m/%Y")

# Data anterior há uma semana
previous_date = date - dt.timedelta(weeks=1)

# Obtém o horário atual em formato UTC usando a função 'get_utc_time' do módulo 'utils'
hour = get_utc_time()

def main():
    """
    Obtém os dados das estações automáticas do INMET, com base na data atual e hora.
    """
    # Obtém os dados das estações automáticas do INMET com base na data e hora
    time_data = get_data_times(date, hour)
    print(time_data)

    # Separando o resultado
    data_split = split_dataframe_stations_inmet(time_data)

    # Salvando em json e realizando o upload no SFTP
    for cod_station, data_station in data_split.items():
        # Define o nome dos arquivo com base na data atual e hora
        file_name = f"inmet_{cod_station}_{date}_{hour}.json"
        save_json(data_station, file_name)

    return 0

def main1():
    """
    Obtém os dados das estações manuais do INMET, com base na data atual e na data anterior há uma semana
    """
    # Define o nome dos arquivo com base na data atual e na data anterior
    file_name_manuals = f"inmet_{date}_{previous_date}.json"

    # Obtém os dados do INMET (estações MANUAIS) com base na data atual e na anterior há uma semana
    data_manuals = get_data_manuals(date, previous_date)
    print(data_manuals)

    # Separando o resultado
    data_split = split_dataframe_stations_inmet(data_manuals)

    # Salvando em json e realizando o upload no SFTP
    for cod_station, data_station in data_split.items():
        # Define o nome dos arquivo com base na data atual e hora
        file_name_manuals = f"inmet_{cod_station}_{date}_{previous_date}.json"
        save_json(data_station, file_name_manuals)

    return 0

def main2():
    data_processor = DataProcessor(institute_id=3)
    data_processor.run()

def main3():
    """
    Obtém os dados de todas as estações da ANA que retornam de hora em hora e 30 em 30 minutos, com base na data atual
    """
    # Lista com os códigos das estações que retornam de hora em hora e 30 em 30 minutos
    codes_stations_hour_thirty = [
        '57739000', '57562000', '57555800', '57555500',
        '57119000', '56992480', '56992400', '56992380',
        '56992370', '56991380', '56991350', '56991300',
        '57836000', '57774000', 
        '57769000', '57765000',
        '57730000', '57435000',
        '57415000', '57410000',
        '57390000', '57370005',
        '57256000', '57155000',
        '57151000', '57150500'
    ]

    intervals_hour_thirty = [
        'Hora', 'Hora', 'Hora', 'Hora',
        'Hora', 'Hora', 'Hora', 'Hora',
        'Hora', 'Hora', 'Hora', 'Hora',
        '30 minutos', '30 minutos',
        '30 minutos', '30 minutos',
        '30 minutos', '30 minutos',
        '30 minutos', '30 minutos',
        '30 minutos', '30 minutos',
        '30 minutos', '30 minutos',
        '30 minutos', '30 minutos'
    ]

    # Define o nome do arquivo com base na data e hora
    file_name_hour = f"ana_hora_trinta_{date}_{hour}.json"

    # Obtém os dados da ANA (hora e 30 em 30)
    data_hour_thirty = get_data_ana(formatted_date, codes_stations_hour_thirty, intervals_hour_thirty)
    print(data_hour_thirty)

    # Salva os daods em formato JSON no arquivo especificado
    save_json(data_hour_thirty, file_name_hour)

    return 0

def main4():
    """
    Obtém os dados de todas as estações da ANA que retornam de 15 em 15 minutos, com base na data atual
    """

    # Lista com os códigos das estações que retornam de 15 em 15 minutos
    codes_stations_fifteen = [
        '57830000', '57552000', '57480000', '57474000', '57473500', '57440000',
        '57430000', '57420000', '57413000', '57370030', '57370010', '57200000',
        '57120080', '57119500', '57118080', '57117000', '56994500', '55810000'
    ]

    intervals_fifteen = [
        '15 minutos', '15 minutos', '15 minutos', '15 minutos', '15 minutos', '15 minutos',
        '15 minutos', '15 minutos', '15 minutos', '15 minutos', '15 minutos', '15 minutos',
        '15 minutos', '15 minutos', '15 minutos', '15 minutos', '15 minutos', '15 minutos'
    ]
    #intervals_fifteen = ['15 minutos' for _ in range(18)]


    # Define o nome do arquivo com base na data e hora
    file_name_fifteen = f"ana_quinze_{date}_{hour}.json"

    # Obtém os dados da ANA (hora e 30 em 30)
    data_fifteen = get_data_ana(formatted_date, codes_stations_fifteen, intervals_fifteen)
    print(data_fifteen)

    # Salva os daods em formato JSON no arquivo especificado
    save_json(data_fifteen, file_name_fifteen)

    return 0

if __name__ == "__main__":
    # Agendando main() para rodar a cada hora, começando 15 minutos após a hora
    schedule.every().hour.at(":15").do(main)

    # Agendando main() para rodar a cada hora, começando 15 minutos após a hora, porem inserindo no banco
    #schedule.every().hour.at(":15").do(main2)

    # Agendando main1() para rodar toda segunda-feira às 3 da manhã
    schedule.every().monday.at("03:00").do(main1)

    while True:
        schedule.run_pending()
        time.sleep(60)