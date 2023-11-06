import logging
import requests
import lxml.etree
import pandas as pd

from config.api_config import API_URL_ANA

def get_data_ana(current_date: str, code_stations: list, intervals: list) -> pd.DataFrame | None:
    """Obtém dados horários referentes a estações selecionadas da ANA de um dia

    Args:
        current_date (str): Data para consulta (formato "DD-MM-YYYY")
        code_stations (list): Lista com os códigos das estações a serem consultadas 
        intervals (list): Lista com os intervalos respectivos a cada estação

    Returns:
        pd.DataFrame | None: Retorna um DataFrame contendo as informações ou None em caso de erro.
    """
    try:
        end_date = ""
        df_ana = pd.DataFrame(columns=["Instituição", "DataHora", "Vazao", "Nivel", "Chuva", "CodEstacao", "Intervalo"])

        for code_station, interval in zip(code_stations, intervals):
            url = f"{API_URL_ANA}codEstacao={code_station}&dataInicio={current_date}&dataFim={end_date}"

            response = requests.get(url)
            response.raise_for_status()

            # Converte o resultado da resposta que está em XML para bytes
            result_bytes = response.text.encode()

            # Converte o resultado para um objeto ElementTree
            root = lxml.etree.fromstring(result_bytes)

            if interval == 'Hora':
                data_items = root.findall(".//DadosHidrometereologicos")[:1]
            elif interval == '30 minutos':
                data_items = root.findall(".//DadosHidrometereologicos")[:2]
            elif interval == '15 minutos':
                data_items = root.findall(".//DadosHidrometereologicos")[:4]

            if data_items:
                for get_first in data_items:
                    date_hour = get_first.find(".//DataHora").text.strip() if get_first.find(".//DataHora") is not None else None
                    flow_element = get_first.find(".//Vazao")
                    flow = flow_element.text.strip() if flow_element is not None and flow_element.text is not None else None
                    river_level_element = get_first.find(".//Nivel")
                    river_level = river_level_element.text.strip() if river_level_element is not None and river_level_element.text is not None else None
                    rain_element = get_first.find(".//Chuva")
                    rain = rain_element.text.strip() if rain_element is not None and rain_element.text is not None else None

                    df = pd.DataFrame({"Instituição": ["ANA"], "DataHora": [date_hour], "Vazao": [flow], "Nivel": [river_level], "Chuva": [rain], "CodEstacao": [code_station], "Intervalo": [interval]})
                    df_ana = pd.concat([df_ana, df], ignore_index=True)

                    logging.info(
                        f"Dados requisitados com sucesso! - Status: {response.status_code}"
                    )
        df_ana = convert_utc_ana(df_ana)
        return df_ana
            
    except requests.exceptions.RequestException as error:
        logging.error(
            f"Erro na solicitação HTTP para a estação {code_station}: {error}"
        )
        return None
    except lxml.etree.XMLSyntaxError as error:
        logging.error(
            f"Erro ao analisar o XML da estação {code_station}: {error}"
        )
        return None
    
def convert_utc_ana(df_ana: pd.DataFrame) -> pd.DataFrame:
    """
    Converte as informações de data e hora em um DataFrame da ANA (Agência Nacional das Águas)
    para o horário local do Espírito Santo (ES) e retorna o DataFrame resultante com timestamps Unix.

    Args:
        df_ana (pd.DataFrame): Um DataFrame contendo os dados da ANA.

    Returns:
        pd.DataFrame: Um DataFrame com as informações de data e hora convertidas para o horário local do ES
                      e representadas como timestamps Unix (segundos desde 1970-01-01 00:00:00 UTC) como int32.
    """
    # Converte a coluna DataHora para um objeto Datetime
    df_ana["DataHora"] = pd.to_datetime(df_ana["DataHora"], format="%Y-%m-%d %H:%M:%S")

    # Converte a coluna "DATA_HORA" para timestamp Unix (segundos desde 1970-01-01 00:00:00 UTC) como int32
    df_ana["DataHora"] = pd.to_datetime(df_ana["DataHora"]).astype("int64") // 10**9
    df_ana["DataHora"] = df_ana["DataHora"].astype("int32")

    # Retorna o Dataframe com horario timestamp convertido
    return df_ana