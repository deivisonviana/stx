import pandas as pd
import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
import inmet

def df_temp(data_inicial, data_final, cod_estacao):
    df = inmet.sync_converter_router(data_inicial, data_final, cod_estacao)
    df['TEM_MIN'] = pd.to_numeric(df['TEM_MIN'], errors='coerce')
    df['TEM_MAX'] = pd.to_numeric(df['TEM_MAX'], errors='coerce')
    df['TEM_INS'] = pd.to_numeric(df['TEM_INS'], errors='coerce')
    grouped_df = df.groupby(['DC_NOME', 'DT_MEDICAO'])
    return grouped_df

def periodo_absoluto(data_inicial, data_final, cod_estacao):
    grouped_df = df_temp(data_inicial, data_final, cod_estacao)
    df = grouped_df.agg({'TEM_MIN': 'min', 'TEM_MAX': 'max', 'TEM_INS': 'mean'}).reset_index()
    df['TEM_INS'] = df['TEM_INS'].round()
    return df

def periodo_media(data_inicial, data_final, cod_estacao):
    grouped_df = df_temp(data_inicial, data_final, cod_estacao)
    df = grouped_df.agg({'TEM_MIN': 'mean', 'TEM_MAX': 'mean', 'TEM_INS': 'mean'}).reset_index()
    df['TEM_INS'] = df['TEM_INS'].round()
    return df

def graf_temp(df):
    # Calculate the average temperature
    df['TEM_MEDIA'] = (df['TEM_MIN'].astype(float) + df['TEM_MAX'].astype(float)) / 2

    # Get unique station names from the DataFrame
    unique_stations = df['DC_NOME'].unique()

    # Iterate over each unique station and create a separate plot
    for station in unique_stations:
        station_df = df[df['DC_NOME'] == station]

        # Create a new figure for each station
        fig, ax = plt.subplots(figsize=(14, 6))

        plt.plot(station_df['DT_MEDICAO'], station_df['TEM_MIN'], marker='o', linestyle='-', color='b', label='Temperatura Mínima')
        plt.plot(station_df['DT_MEDICAO'], station_df['TEM_MAX'], marker='o', linestyle='-', color='r', label='Temperatura Máxima')
        plt.plot(station_df['DT_MEDICAO'], station_df['TEM_MEDIA'], marker='o', linestyle='-', color='g', label='Temperatura Média')

        # Configure plot settings
        ax.set(xlabel='Dias (dd/mm/aa)', ylabel='Temperatura($\degree$C)', title=f'Temperatura média do ar em {station}')
        ax.grid(True)
        ax.tick_params(axis='x', which='both', labelrotation=45)

        # Add a legend
        ax.legend(frameon=True, loc='best', prop={'size': 12})

        # Show the plot
        plt.show()