import json
import pandas as pd

from config.app_config import TIME_ZONE


def extract_data(raw_data: pd.DataFrame, mapping: pd.DataFrame):
    """
    Extrai e transforma dados brutos em um formato específico de acordo com um mapeamento fornecido.

    Args:
        raw_data (dict): Dados não processados provenientes de fontes como FTPs e APIs.
        mapping (dict): Um dicionário que define como os campos de dados brutos devem ser mapeados
                        para campos específicos do resultado.

    Returns:
        list: Uma lista de dicionários contendo os dados extraídos, formatados e mapeados.
    """
    # Inicializa uma lista vazia para armazenar os dados extraídos
    extracted_data_list = []  

    # Converte a data e hora brutos em um formato desejado
    timestamp = convert_time(raw_data[mapping["date"]], raw_data[mapping["hour"]])

    # Itera sobre as linhas do DataFrame de mapeamento
    for _, row in mapping.iterrows():
        # Carrega a configuração JSON da linha
        config_dict = json.loads(row['config'])

        variable_data = {}  # Inicializa um dicionário para armazenar os dados da variável

        # Itera sobre as variáveis e seus respectivos mapeamentos
        for key, value in config_dict['variables'].items():
            instant_key = value['instant']
            maximun_key = value['maximun']
            minimun_key = value['minimun']
            average_key = value['average']

            # Obtém os valores brutos da variável a partir das chaves fornecidas
            instant = raw_data.get(instant_key, None)
            maximun = raw_data.get(maximun_key, None)
            minimun = raw_data.get(minimun_key, None)
            average = raw_data.get(average_key, None)

            # Substitui NaN (valores ausentes) por None
            instant = None if pd.isna(instant) else instant
            maximun = None if pd.isna(maximun) else maximun
            minimun = None if pd.isna(minimun) else minimun
            average = None if pd.isna(average) else average

            # Armazena os valores da variável em um dicionário
            variable_data[key] = {
                'instant': instant,
                'maximun': maximun,
                'minimun': minimun,
                'average': average
            }

        # Itera sobre os dados da variável e cria um dicionário de dados finais para cada variável
        for key, value in variable_data.items():
            if value:
                data_dict = {
                    "date_hour": timestamp,
                    "instant": value['instant'],
                    "maximun": value['maximun'],
                    "minimun": value['minimun'],
                    "average": value['average'],
                    "id_station": row['id'],
                    "id_variable": key,
                    "id_flag": 5,
                }
                # Adiciona o dicionário de dados à lista de dados extraídos
                extracted_data_list.append(data_dict)

    return extracted_data_list  # Retorna a lista de dados extraídos


def convert_time(date: str, hour: str):
    # Combina os parâmetros "date" e "hour" em uma única coluna "DATA_HORA" no formato 'YYYY-MM-DD HH:MI:SS'
    date_time_str = date + " " + hour[:-2] + ":" + hour[-2:]

    # Converte 'DATA_HORA' para datetime
    date_time = pd.to_datetime(
        date_time_str, format="%Y-%m-%d %H:%M", utc=True)

    # Converte a coluna "DATA_HORA" para a hora local usando o fuso horário do ES (Espírito Santo)
    date_time_local = date_time.tz_convert(TIME_ZONE)

    # Converte a coluna "DATA_HORA" para uma string no formato desejado 'YYYY-MM-DD HH:MI:SS TZ'
    return date_time_local.strftime("%Y-%m-%d %H:%M:%S %Z")
