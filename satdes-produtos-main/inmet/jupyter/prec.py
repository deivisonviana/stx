import pandas as pd
import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
import inmet


def precipitacao(data_inicial, data_final, cod_estacao):
    df = inmet.sync_converter_router(data_inicial, data_final, cod_estacao)
    df['CHUVA'] = pd.to_numeric(df['CHUVA'], errors='coerce')
    grouped_df = df.groupby(['DC_NOME', 'DT_MEDICAO'])
    grouped_df = grouped_df.agg({'CHUVA': 'sum'}).reset_index()
    return grouped_df

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