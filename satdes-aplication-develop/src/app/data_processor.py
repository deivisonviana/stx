import requests
import pandas as pd
import datetime as dt
import json

from app import get_data_times
from utils import get_utc_time, extract_data

from config import API_URL_SATDES


class DataProcessor:
    
    def __init__(self, institute_id: str):
        """
        Inicializa o objeto DataProcessor.

        Args:
            institute_id (int): ID do instituto.
        """
        self.source_url = API_URL_SATDES
        self.institute_id = institute_id
        self.station_config = self.get_station_config()
        self.date = dt.datetime.today().date()
        self.hour = get_utc_time()
        self.file_name = f"{self.date}_{self.hour}.json"
        

    def get_station_config(self):
        """
        Obtém a configuração da estação a partir da fonte de dados.

        Returns:
            pd.DataFrame: DataFrame contendo a configuração da estação.
        """
        url = self.source_url + f'/stations/institute/{self.institute_id}'

        try:
            response = requests.get(url=url, timeout=10, verify=False)
            response.raise_for_status()  # Lança uma exceção se a resposta não for bem-sucedida

        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter configuração da estação: {e}")

        else:
            config_data = response.json()

            return pd.DataFrame(config_data['data'])

    def fetch_station_data(self):
        """
        Obtém os dados da estação e os salva em um arquivo JSON.

        Returns:
            dict: Dados da estação.
        """
        return get_data_times(self.date, self.hour)


    def process_station_data(self, station_data: pd.DataFrame):
        """
        Processa os dados da estação de acordo com a configuração.

        Args:
            station_data (pd.DataFrame): DataFrame contendo os dados da estação.

        Returns:
            list: Lista de dados processados.
        """
        data = []

        merged_data = station_data.merge(self.station_config, left_on='CD_ESTACAO', right_on='code')
       
        for _, row in merged_data.iterrows():
            config = row.to_frame().T
            
            if not config.empty:
                data.append(extract_data(row, config))
        
        return data


    def send_data_to_api(self, data):
        """
        Envia os dados processados para uma API.

        Args:
            data (list): Lista de dados processados.

        Returns:
            requests.Response: Resposta da API.
        """
        url = self.source_url + "/records"

        data = json.dumps({'records': data})
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(url=url, data=data, headers=headers,  verify=False)
            response.raise_for_status()  # Lança uma exceção se a resposta não for bem-sucedida

            return response

        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar dados para a API: {e}")

    def run(self):
        """
        Executa o processo de coleta, processamento e envio de dados.
        """
        try:
            station_data = self.fetch_station_data()
            data = self.process_station_data(station_data)
            response = self.send_data_to_api(data)

            print(response.content)

        except Exception as e:
            print(f"Erro ao executar o processo: {e}")


if __name__ == "__main__":
    # Exemplo de uso com diferentes fontes de dados
    data_processor = DataProcessor(institute_id=3)

    data_processor.run()
