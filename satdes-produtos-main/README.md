# Documentação do Repositório Satdes-Produtos

## Introdução

O repositório Satdes-Produtos é uma plataforma dedicada ao processamento, análise e visualização de dados meteorológicos de várias instituições, incluindo o INCAPER, CEPDEC e INMET. Este documento visa detalhar a pasta "Jupyter (Produtos Meteorológicos)" e os arquivos principais para criação das rotas Flask do repositório, que desempenha um papel crucial no processamento e geração de informações meteorológicas específicas.

## Rotas API Flask (route.py)

Os scripts principais, compõe uma aplicação web Flask que permite aos utilizadores recuperar e exibir vários dados relacionados com o clima. Esta aplicação fornece informações sobre temperatura, humidade, precipitação, dados de vento e evapotranspiração para intervalos de tempo específicos. Os calculos são executados em cada umas das rotas, e esta presente no script functions.py

### 1. **Rotas e Recursos**:

- **/ (Página Inicial):** Apresenta a string 'Boletim Meteorológico'.

- **/temp_hora (Temperatura por Hora):** Recupera e exibe dados de temperatura para um intervalo de datas específico, por hora.

- **/temp_dia (Temperatura por Dia):** Recupera e exibe dados de temperatura para um intervalo de datas específico, por dia.

- **/umi_hora (Humidade por Hora):** Recupera e exibe dados de humidade para um intervalo de datas específico, por hora.

- **/umi_dia (Humidade por Dia):** Recupera e exibe dados de humidade para um intervalo de datas específico, por dia.

- **/prec (Precipitação):** Recupera e exibe dados de precipitação para um intervalo de datas específico.

- **/rosa_vento (Dados de Vento):** Recupera e exibe dados de direção e velocidade do vento para um intervalo de datas específico.

- **/evapo (Evapotranspiração):** Recupera e exibe dados de evapotranspiração para um intervalo de datas específico.

### 2. **Executando o Aplicativo**:

Aqui estão alguns exemplos de utilização das rotas da aplicação:

- **Para ver os dados de temperatura por hora, visite:** http://localhost:5000/temp_hora

- **Para ver os dados de humidade por dia, visite:** http://localhost:5000/umi_dia

Pode aceder a outras rotas de forma semelhante, substituindo o caminho da rota pelo que deseja.

Sinta-se à vontade para personalizar os intervalos de datas e as fontes de dados na sua aplicação para se adequarem às suas necessidades específicas.


## Produtos Meteorológicos (Jupyter)

A pasta "Jupyter (Produtos Meteorológicos)", foi criada para realizar os cálculos, análises e geração de produtos relacionados a dados meteorológicos utilizando a biblioteca pandas. Dentro da pasta jupyter, cada script tem um objetivo específico:

### 1. **inmet.py**:
   - Este script é responsável por recuperar dados meteorológicos brutos via API do INMET (Instituto Nacional de Meteorologia).
   - Funcionalidades:
     - Variáveis globais armazenam informações como token de autenticação para a API do INMET e URLs de acesso aos dados.
     - Funções incluem a conversão de horas, datas e recuperação de informações sobre estações meteorológicas.
     - A função principal `sync_converter_router` recupera e processa dados meteorológicos para criação de DataFrames consolidados.

### 2. **temp.py**:
   - Script dedicado ao processamento de dados de temperatura, incluindo temperatura mínima, máxima e média do ar.
   - Funcionalidades:
     - `df_temp(data_inicial, data_final, cod_estacao)`: Recupera dados de temperatura para uma estação específica dentro de um intervalo de datas.
     - `periodo_absoluto(data_inicial, data_final, cod_estacao)`: Calcula estatísticas de temperatura (mínima, máxima e média).
     - `periodo_media(data_inicial, data_final, cod_estacao)`: Calcula estatísticas de temperatura média.
     - `graf_temp(df)`: Gera gráficos de temperatura ao longo do tempo.

### 3. **umi.py**:
   - Script voltado para o processamento de dados de umidade relativa do ar.
   - Funcionalidades:
     - `df_umidade(data_inicial, data_final, cod_estacao)`: Recupera dados de umidade relativa do ar para uma estação específica dentro de um intervalo de datas.
     - `periodo(data_inicial, data_final, cod_estacao)`: Calcula estatísticas de umidade relativa (mínima, máxima e média).
     - `periodo_media(data_inicial, data_final, cod_estacao)`: Calcula estatísticas de umidade relativa média.
     - `graf(df)`: Gera gráficos de umidade relativa do ar ao longo do tempo.

### 4. **vento.py**:
   - Script focado em dados de direção e velocidade do vento, com ênfase na geração de gráficos de rosa dos ventos.
   - Funcionalidades:
     - `periodo(data_inicial, data_final, cod_estacao)`: Recupera dados de direção e velocidade do vento.
     - `graf(df)`: Gera gráficos de rosa dos ventos para visualização da distribuição do vento em diferentes direções.

### 5. **evapo.py**:
   - Script para o cálculo de radiação solar.
   - Funcionalidades:
     - `radiacao(data_inicial, data_final, cod_estacao)`: Recupera dados meteorológicos e calcula a radiação solar diária para uma estação específica, para a geração do calculo de avapotranspiração.
     - `graf_radiacao(df)`: Gera gráficos da radiação solar ao longo do tempo.

## Uso

O uso dos scripts da seção "Produtos Meteorológicos (Jupyter)" envolve várias etapas:

1. **Configuração Inicial**:
   - Garanta que todas as bibliotecas Python necessárias estejam instaladas no seu ambiente.

2. **Configuração da API**:
   - Obtenha uma chave de API (Token) válida para a API do INMET e armazene-a onde necessário nos scripts `inmet.py`.

3. **Execução de Scripts**:
   - Importe as bibliotecas necessárias nos scripts Jupyter.
   - Configure os parâmetros, como datas de início e fim, códigos de estações, etc.
   - Execute as funções apropriadas para recuperar, processar e analisar os dados meteorológicos.

4. **Visualização de Resultados**:
   - Utilize os DataFrames resultantes e os gráficos gerados para análise e visualização de dados meteorológicos.

## Requisitos

Cada script especifica as bibliotecas Python necessárias. Certifique-se de que todas essas bibliotecas estejam instaladas no seu ambiente Python antes de executar os scripts.

## Notas Finais

Os scripts da seção "Produtos Meteorológicos (Jupyter)" são uma ferramenta poderosa para processamento e análise de dados meteorológicos. Eles podem ser personalizados para diferentes estações meteorológicas e intervalos de tempo, permitindo a geração de informações e gráficos informativos sobre as condições meteorológicas ao longo do tempo. Certifique-se de seguir as instruções fornecidas na documentação e verificar se todos os requisitos estão atendidos antes de executar os scripts relacionados a dados meteorológicos.

