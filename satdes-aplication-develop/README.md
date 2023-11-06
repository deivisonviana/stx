# Documentação do Repositório Satdes-Application

Este repositório é responsável por armazenar os scripts (jobs) que coletam os dados brutos meteorológicos das instituições que fazem parte do projeto, a saber:

* INCAPER - Instituto Capixaba de Pesquisa, Assistência Técnica e Extensão Rural;
* CEPDEC - Coordenadoria Estadual de Proteção e Defesa Civil;
* INMET - Instituto Nacional de Meteorologia;
* ANA - Agência Nacional de Águas e Saneamento Básico;
* AGERH ES - Agência Estadual de Recursos Hídricos do Espírito Santo;

## Formas de Envio de Dados de Cada Instituição

Esses dados são obtidos de duas maneiras: por meio de API (Interface de Programação de Aplicativos) ou acessando os servidores FTP (Protocolo de Transferência de Arquivos) da instituição.

No caso, o INMET e a ANA disponibilizam esses dados por meio de APIs, diferente do INCAPER e da CEPDEC que é por meio de acesso ao sevidor FTP.

A AGERH por sua vez tem um caso diferente das demais, retornam dados por meio da API da ANA e por meio de um servidor FTP.

## Sobre as APIs

A API da ANA (que contém os dados da AGERH) é pública, permitindo que qualquer pessoa acesse esses dados. Para adquirir esses dados, basta acessar o web service [Web Service ANA](http://telemetriaws1.ana.gov.br/ServiceANA.asmx).

Já a API do INMET é restrita, sendo necessário solicitar uma chave de API (Token) e especificar as informações desejadas ao INMET. Para fazer essa solicitação, acesse o [Manual de API - INMET](https://portal.inmet.gov.br/manual/manual-de-uso-da-api-estações).

## Sobre os Servidores FTP

AGERH, INCAPER e CEPDEC utilizam servidores FTP para armazenar e distribuir os dados. Para acessar esses dados, é necessário entrar em contato com a instituição para solicitar os dados desejados, especificando o(s) dado(s), período e motivo da solicitação.

Contato AGERH - ES: protocolo@agerh.es.gov.br ou (27) 3347-6200

Contato INCAPER: clima@incaper.es.gov.br ou (27) 3636-9882 / (27) 3636-9883

Contato CEPDEC: defesacivil@bombeiros.es.gov.br ou (27) 3194-3697

# Desenvolvimento

Nesta seção, registraremos os detalhes do desenvolvimento dos scripts que coletam os dados das instituições.

Inicialmente, esses scripts são jobs (tarefas agendadas) que, na maioria das vezes, são executados a cada hora. Cada instituição possui suas particularidades, e, por isso, a seção foi subdividida para explicar as particularidades de cada órgão que faz parte do projeto.

Esses scripts foram desenvolvidos em Python e modularizados em pastas para facilitar a integração dos códigos. As pastas estão nomeadas da seguinte forma:

* [logs](https://github.com/incaper/satdes-aplication/tree/develop/logs): contém arquivos relacionados ao tratamento de erros e acertos;
* [src](https://github.com/incaper/satdes-aplication/tree/develop/src): esta pasta contém o arquivo principal ([main.py](https://github.com/incaper/satdes-aplication/blob/develop/src/main.py)) e possui subpastas, a saber:
  * [app](https://github.com/incaper/satdes-aplication/tree/develop/src/app): armazena scripts que contêm as funções responsáveis por coletar os dados das instituições;
  * [config](https://github.com/incaper/satdes-aplication/tree/develop/src/config): armazena arquivos de configuração com variáveis privadas (usando a biblioteca `os` e arquivos .env);
  * [utils](https://github.com/incaper/satdes-aplication/tree/develop/src/utils): armazena funções comuns que podem ser utilizadas em várias ações;
* [raiz](https://github.com/incaper/satdes-aplication/tree/develop): arquivos de documentação.

## INCAPER

### Requisitos

Texto

### Arquitetura

Texto

### Implementação

Texto

### Testes

Texto

## CEPDEC

### Requisitos

Texto

### Arquitetura

Texto

### Implementação

Texto

### Testes

Texto

## INMET

O INMET retorna os dados meteorológicos de estações manuais e automáticas. No caso do Espírito Santo, possuímos três estações manuais e quatorze automáticas.

### Requisitos

* As automáticas retornam dados a cada hora (sempre depois de 15 minutos), passando como parâmetros a data, hora e token;
* Já as manuais possuem muitos dados faltantes e não garantem a entrega dos dados. Além disso, a API é diferente das automáticas. Para obter esses dados, é preciso passar como parâmetros o período (data inicial e data final), o código da estação e o token.

### Arquitetura

No arquivo [data_inmet.py](https://github.com/incaper/satdes-aplication/blob/develop/src/app/data_inmet.py), estão as funções `get_data_times`, `get_data_manuals` e `convert_utc_inmet`. Estas funções fazem o seguinte:

  * `get_data_times`: função responsável por coletar os dados meteorológicos das estações automáticas a cada hora. Ela retorna um DataFrame com os dados ou `None` se não houver resposta da API;
  * `get_data_manuals`: função responsável por coletar os dados meteorológicos das estações manuais semanalmente. Ela também retorna um DataFrame com os dados ou `None` se não houver resposta da API;
  * `convert_utc_inmet`: função responsável por converter as informações de data e hora (que estão em UTC) para timestmp e também adiciona um identificador de instituição (coluna INMET). Ela retorna o DataFrame convertido.

### Implementação

No arquivo [main.py](https://github.com/incaper/satdes-aplication/blob/develop/src/main.py), foram criadas duas funções principais, uma para coletar os dados das estações automáticas e outra para coletar os dados das estações manuais.

Essas funções foram divididas porque é necessário que a função das automáticas seja executada nos 15 minutos de cada hora, por exemplo:

* 12:15;
* 13:15;
* 14:15.

A função que lida com as estações manuais é executada semanalmente, às segundas-feiras, às 03:00 da manhã. Portanto, o intervalo de coleta para as estações manuais é de uma semana, devido à escassez de dados.

Essa configuração de tempo foi feita utilizando a biblioteca `schedule` do Python. É necessário que o programa seja executado uma vez para entrar em um loop "infinito".

Para agendar a execução no Windows Task Scheduler, configure a tarefa para ser disparada diariamente, começando nos 15 minutos da hora desejada e repetindo a cada hora.

Ambas as funções retornam DataFrames convertidos em um arquivo .JSON pela função `save_json`, essa função também chama outra função responsável por colocar esse arquivo .JSON (arquivo esse, contendo o dado de uma estação daquele período informado) gerado em um servidor SFTP (`upload_sftp`).É preciso configurar as variáveis que estão no arquivo .env.example em um arquivo .env.

### Testes

Foram realizados testes de execução, e os arquivos gerados atendem aos requisitos desejados. Seguem exemplos desses arquivos .JSON:

* Manuais: [inmet2023-09-13_2023-09-06.json](https://github.com/incaper/testes/blob/inmet/TesteInmet/inmet2023-09-14_2023-09-07.json)

* Automáticas: [inmet2023-09-13_1200.json](https://github.com/incaper/testes/blob/inmet/TesteInmet/inmet2023-09-13_1200.json)

## ANA

A ANA disponibiliza dados hidrológicos de 65 estações, divididas por intervalos de medição: 24 estações fazem leituras a cada hora, 17 a cada 30 minutos e 24 a cada 15 minutos.

Nem todas as estações retornam os 3 dados das estações (vazão, nível e chuva), ao todo são 38 estações que retornam todos os dados, e todas as estações retornam o nível.

### Requisitos

* Ficou decidido que será criado um script para rodar a cada hora e coletar os dados de todas as estações. Dentro do arquivo JSON, os dados das estações que são medidas a cada hora terão um dado para cada estação, aquelas que são medidas a cada 30 minutos terão dois dados para cada estação e as que são medidas a cada 15 minutos terão quatro dados para cada estação.
* Além disso, nem sempre as estações retornarão o último dado corretamente; muitas têm dados vazios ou atrasos no envio. Esse problema será tratado com um script para verificar dados faltantes.

### Arquitetura

No arquivo [data_ana.py](https://github.com/incaper/satdes-aplication/blob/develop/src/app/data_ana.py), você encontrará as funções `get_data_ana` e `convert_utc_ana`, que desempenham as seguintes funções:

* `get_data_ana`: Esta função é responsável por coletar os dados hidrológicos das estações da ANA. Ela recebe como parâmetros a data inicial, a lista de códigos das estações e uma lista de intervalos de tempo para cada estação. A função retorna um DataFrame com os dados ou None se a API não responder;
* `convert_utc_ana`: Esta função é responsável por converter as informações de data e hora (que já estão no horário local) para formato de timestamp. Ela retorna o DataFrame convertido.

### Implementação

No arquivo [main.py](https://github.com/incaper/satdes-aplication/blob/develop/src/main.py), foi criada duas funções principais (`main3()`e `main4()`) para coletar os dados de todas as estações.

As estações são definidas por uma lista de códigos, o que torna fácil adicionar ou remover estações quando necessário.

A coleta dos dados segue a mesma lógica do INMET e ocorre a cada 15 minutos de cada hora. Uma lista auxiliar informa o intervalo de tempo de cada estação, mantendo a ordem da lista de códigos.

A configuração do agendamento utiliza a biblioteca Python schedule. O programa entra em um loop "infinito" e é necessário executá-lo uma vez para que os agendamentos funcionem.

Para agendar a execução no Windows Task Scheduler, configure a tarefa para ser acionada diariamente, começando 15 minutos após a hora desejada e repetindo a cada hora.

A função principal retorna um DataFrame que é convertido em um arquivo JSON. As variáveis de configuração estão no arquivo .env.example e devem ser configuradas em um arquivo .env.

### Testes

Foram realizados testes de execução, e os arquivos gerados atendem aos requisitos desejados. Aqui estão exemplos desses arquivos .JSON e um arquivo .xlsx para visualização dos dados:

* Teste Final JSON: [ana2023-09-26_1800.json](https://github.com/incaper/testes/blob/ana/TesteANA/ana2023-09-26_1800.json)
* Teste Parcial: [ana2023-09-26_1500.json](https://github.com/incaper/testes/blob/ana/TesteANA/ana2023-09-26_1500.json)
* Teste Hora: [anaHora2023-09-26_1200.json](https://github.com/incaper/testes/blob/ana/TesteANA/anaHora2023-09-26_1200.json)
* Teste 30 em 30: [anaTrinta2023-09-26_1200.json](https://github.com/incaper/testes/blob/ana/TesteANA/anaTrinta2023-09-26_1200.json)
* Teste 15 em 15: [anaQuinze2023-09-26_1200.json](https://github.com/incaper/testes/blob/ana/TesteANA/anaQuinze2023-09-26_1200.json)
* Teste Parcial em xlsx: [anaTesteParcial.xlsx](https://github.com/incaper/testes/blob/ana/TesteANA/anaTesteFinal%20(1).xlsx)
* Teste Final em xlsx: [anaTesteFinal.xlsx](https://github.com/incaper/testes/blob/ana/TesteANA/anaTesteAgoraVai.xlsx)

## AGERH - ES

### Requisitos

Texto

### Arquitetura

Texto

### Implementação

Texto

### Testes

Texto
