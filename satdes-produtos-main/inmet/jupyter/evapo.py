import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pyeto
from datetime import datetime
import inmet

def radiacao(data_inicial, data_final, cod_estacao):
    df = inmet.sync_converter_router(data_inicial, data_final, cod_estacao)
    df['TEM_MIN'] = pd.to_numeric(df['TEM_MIN'], errors='coerce')
    df['TEM_MAX'] = pd.to_numeric(df['TEM_MAX'], errors='coerce')
    df['TEM_INS'] = pd.to_numeric(df['TEM_INS'], errors='coerce')
    df['CHUVA'] = pd.to_numeric(df['CHUVA'], errors='coerce')
    df['VL_LATITUDE'] = pd.to_numeric(df['VL_LATITUDE'], errors='coerce')
    grouped_df = df.groupby(['DC_NOME', 'DT_MEDICAO'])
    df = grouped_df.agg({'TEM_MIN': 'min', 'TEM_MAX': 'max', 'TEM_INS': 'mean','VL_LATITUDE': 'mean', 'CHUVA': 'sum'}).reset_index()
    df['TEM_INS'] = df['TEM_INS'].round()
    # Converte a data inicial para um objeto datetime
    data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')

    # Inicializa uma lista vazia para armazenar os valores de evapotranspiração
    evap_values = []

    for index, row in df.iterrows():
        # Obtenha o dia do ano a partir da data da linha
        day_of_year = row['DT_MEDICAO'].timetuple().tm_yday

        # Calcula o ângulo horário do pôr do sol usando a latitude da estação e o dia do ano
        sol_dec = pyeto.sol_dec(day_of_year)
        latitude = pyeto.deg2rad(row['VL_LATITUDE'])  # Converta a latitude para radianos
        sha = pyeto.sunset_hour_angle(latitude, sol_dec)

        # Calcula a inversa da distância relativa entre a Terra e o Sol usando o dia do ano
        ird = pyeto.inv_rel_dist_earth_sun(day_of_year)
        et_rad = pyeto.et_rad(latitude, sol_dec, sha, ird)

        # Calcula a evapotranspiração potencial para a linha atual
        eto = pyeto.hargreaves(row['TEM_MIN'], row['TEM_MAX'], row['TEM_INS'], et_rad)

        # Adiciona o valor calculado à lista de valores de evapotranspiração
        evap_values.append(eto)

    # Adiciona a lista de valores de evapotranspiração ao DataFrame como uma nova coluna
    df['evap'] = evap_values
    return df

def graf_evap(df):
    unique_stations = df['DC_NOME'].unique()

    for station in unique_stations:
        # Filtra o DataFrame para a estação atual
        station_df = df[df['DC_NOME'] == station]

        # Crie um gráfico de linha para a estação atual
        plt.figure(figsize=(10, 6))

        plt.plot(station_df['DT_MEDICAO'], station_df['evap'], marker='o', linestyle='-', color='b', label='Evap')

        plt.legend(loc='upper left')
        plt.xticks(rotation=45)

        # Adicione rótulos e título
        plt.xlabel('Diario')
        plt.ylabel('Evapotranspiração')
        plt.title(f'Variação de Evapotranspiração - Estação: {station}')

        # Adicione uma legenda
        plt.legend()

        # Mostrar o gráfico
        plt.grid(True)
        plt.show()

def graf_prec(df):
    unique_stations = df['DC_NOME'].unique()

    for station in unique_stations:
        # Filtra o DataFrame para a estação atual
        station_df = df[df['DC_NOME'] == station]

        # Crie um gráfico de linha para a estação atual
        plt.figure(figsize=(20, 6))

        plt.bar(station_df['DT_MEDICAO'], station_df['CHUVA'], color='b', label='Volume de chuva diário')

        plt.legend(loc='upper left')
        plt.xticks(rotation=45)

        # Adicione rótulos e título
        plt.xlabel('Diario')
        plt.ylabel('Precipitação(mm)')
        plt.title(f'Volume de Chuva Diária - Estação: {station}')

        # Adicione uma legenda
        plt.legend()

        # Mostrar o gráfico
        plt.grid(axis='y')  # Adicionei grid apenas no eixo y para gráficos de barras
        plt.show()

def graf_prec_evap(df):
    unique_stations = df['DC_NOME'].unique()

    for station in unique_stations:
        # Filtra o DataFrame para a estação atual
        station_df = df[df['DC_NOME'] == station]

        # Criar um gráfico de barras
        plt.figure(figsize=(20, 6))

        # Plotar a precipitação em barras com a legenda
        bar = plt.bar(station_df['DT_MEDICAO'], station_df['CHUVA'], color='b', label='Precipitação')

        # Criar um segundo eixo y para a evaporação
        ax2 = plt.twinx()

        # Plotar a evaporação em uma linha
        line = ax2.plot(station_df['DT_MEDICAO'], station_df['evap'], marker='o', linestyle='-', color='r', label='Evaporação')

        # Adicionar rótulos e título
        plt.xlabel('Diário')
        plt.ylabel('Precipitação')
        ax2.set_ylabel('Evapotranspiração (mm day-1)')
        plt.title(f'Precipitação e Evapotranspiração Diária - Estação: {station}')

        # Mostrar o gráfico
        plt.grid(True, axis='y')  # Adicionei grid apenas no eixo y para gráficos de barras

        # Criar uma legenda separada para a barra azul e para a linha vermelha
        plt.legend([bar], ['Precipitação'], loc='upper left')
        ax2.legend([line[0]], ['Evaporação'], loc='upper right')

        plt.show()
