import pytz
import datetime as dt

from config.app_config import TIME_ZONE

def get_utc_time() -> str:
    """
    Converte a hora local para o formato UTC e retorna a hora em formato de string no formato "HHMM".

    Returns:
        str: Uma string que representa a hora em formato UTC no formato "HHMM".
    """
    # Obtém a data e hora atual no fuso horário local
    local_zone = dt.datetime.now()

    # Converte a data e hora local para o fuso horário UTC (Tempo Universal Coordenado)
    hour_utc = local_zone.astimezone(dt.timezone.utc)

    # Define a hora atual no fuso horário UTC, zerando os minutos, segundos e microssegundos
    current_time = hour_utc.replace(minute=0, second=0, microsecond=0)

    # Retorna os dados em UTC
    return current_time.strftime("%H%M")


def get_tmz_time(date: str, hour: str) -> str:
    """
    Obtém um timestamp com base em uma data e hora específicas em um fuso horário desejado.

    Args:
        date (str): Uma string que representa a data no formato "AAAA-MM-DD".
        hour (str): Uma string que representa a hora no formato "HHMM".

    Returns:
        str: Um timestamp representando a data e hora no fuso horário desejado.

    Note:
        Esta função assume que você definiu previamente a variável `TIME_ZONE` como o fuso horário desejado.
    """
    # Defina o fuso horário UTC
    utc = pytz.UTC

    # Crie objetos de data e hora a partir das strings
    date_time = dt.datetime.strptime(f"{date} {hour}", "%Y-%m-%d %H%M")

    # Aplique o fuso horário desejado ao objeto de data e hora
    date_time = utc.localize(date_time).astimezone(TIME_ZONE)

    # Converta para timestamp
    return date_time.timestamp()

