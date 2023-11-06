import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import inmet


def df_umidade(data_inicial, data_final, cod_estacao):
    df = inmet.sync_converter_router(data_inicial, data_final, cod_estacao)
    df['UMD_MIN'] = pd.to_numeric(df['UMD_MIN'], errors='coerce')
    df['UMD_MAX'] = pd.to_numeric(df['UMD_MAX'], errors='coerce')
    df['UMD_INS'] = pd.to_numeric(df['UMD_INS'], errors='coerce')
    grouped_df = df.groupby(['DC_NOME', 'DT_MEDICAO'])
    return grouped_df

def periodo(data_inicial, data_final, cod_estacao):
    grouped_df = df_umidade(data_inicial, data_final, cod_estacao)
    df = grouped_df.agg({'UMD_MIN': 'min', 'UMD_MAX': 'max', 'UMD_INS': 'mean'}).reset_index()
    df['UMD_INS'] = df['UMD_INS'].round()
    return df

def periodo_media(data_inicial, data_final, cod_estacao):
    grouped_df = df_umidade(data_inicial, data_final, cod_estacao)
    df = grouped_df.agg({'UMD_MIN': 'mean', 'UMD_MAX': 'mean', 'UMD_INS': 'mean'}).reset_index()
    df['UMD_INS'] = df['UMD_INS'].round()
    return df

def graf(df):
    # Calculate the average temperature
    df['UMD_MEDIA'] = (df['UMD_MIN'].astype(float) + df['UMD_MAX'].astype(float)) / 2

    # Get unique station names from the DataFrame
    unique_stations = df['DC_NOME'].unique()

    # Iterate over each unique station and create a separate plot
    for station in unique_stations:
        station_df = df[df['DC_NOME'] == station]

        # Create a new figure for each station
        fig, ax = plt.subplots(figsize=(14, 6))

        plt.plot(station_df['DT_MEDICAO'], station_df['UMD_MIN'], marker='o', linestyle='-', color='b', label='Temperatura Mínima')
        plt.plot(station_df['DT_MEDICAO'], station_df['UMD_MAX'], marker='o', linestyle='-', color='r', label='Temperatura Máxima')
        plt.plot(station_df['DT_MEDICAO'], station_df['UMD_MEDIA'], marker='o', linestyle='-', color='g', label='Temperatura Média')

        # Configure plot settings
        ax.set(xlabel='Dias (dd/mm/aa)', ylabel='Umidade', title=f'Umidade Relativa do Ar em {station}')
        ax.grid(True)
        ax.tick_params(axis='x', which='both', labelrotation=45)

        # Add a legend
        ax.legend(frameon=True, loc='best', prop={'size': 12})

        # Show the plot
        plt.show()
