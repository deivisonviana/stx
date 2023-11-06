import functions as funcoes
import aiohttp
import asyncio
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

data_inicial = '2022-10-17'
data_final = '2022-11-30'

# Consulta as lista de etações cadastradas no inmet
estacoes = funcoes.get_estacoes('T')

# Filtra as estaçõe do Espirito Santo
estacoes = estacoes.groupby("SG_ESTADO").get_group("ES")

# Agrupando somente os codigos das estações em uma lista
cod_estacao = list(estacoes["CD_ESTACAO"])

# Obtendo dados de todas as estações
#result = funcoes.sync_converter_router(data_inicial, data_final, cod_estacao)
#print(result)
# Obtendo dados de apenas uma estação
#result = funcoes.get_dados(data_inicial,data_final,'A657')
#print(result)
result = funcoes.temperatura_dia(data_inicial,data_final,'A612')
print(result)



#result = funcoes.rosa_dos_ventos(data_inicial,data_final,'A612')
#result = funcoes.radiacao(data_inicial,data_final,'A657')
#print(result)

#Montando o grafico

#df = funcoes.graf(result)