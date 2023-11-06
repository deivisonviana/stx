import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import inmet
from windrose import WindroseAxes

def periodo(data_inicial, data_final, cod_estacao):
    df = inmet.sync_converter_router(data_inicial, data_final, cod_estacao)
    df['VEN_DIR'] = pd.to_numeric(df['VEN_DIR'], errors='coerce')
    df['VEN_VEL'] = pd.to_numeric(df['VEN_VEL'], errors='coerce')
    return df[['DC_NOME', 'DT_MEDICAO','VEN_DIR','VEN_VEL']]

def graf(df3):
    unique_stations = df3['DC_NOME'].unique()

    for station in unique_stations:
        # Filtra o DataFrame para a estação atual
        station_df = df3[df3['DC_NOME'] == station]

        # Preparar os dados
        directions = station_df['VEN_DIR']
        speeds = station_df['VEN_VEL']

        # Criar uma figura e um subplot de rosa dos ventos
        plt.figure(figsize=(8, 8))
        ax = WindroseAxes.from_ax()
        ax.bar(directions, speeds, normed=True, opening=0.8, edgecolor='white')

        # Definir os rótulos do eixo de direção
        ax.set_legend()

        # Adicionar título ao gráfico
        plt.title(f"Rosa dos Ventos - Estação: {station}")

        # Exibir o gráfico
        plt.show()

