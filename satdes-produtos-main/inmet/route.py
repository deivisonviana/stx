from flask import Flask, render_template
import os
import functions as funcoes

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Boletim Meteorológico'

# Retorna a temperatura entre 0h a 23h
@app.route('/temp_hora')
def temperatura_hora():
    datai = '2022-11-28'
    dataf = '2022-11-29'
    result = funcoes.temperatura_hora(datai, dataf, 'A612')
    return render_template('tempHR.html', filteredData=result)

# Retorna a temperatura entre intervalo de dias
@app.route('/temp_dia')
def temperatura_dia():
    datai = '2022-10-28'
    dataf = '2022-11-30'
    filteredData = funcoes.temperatura_dia(datai, dataf, 'A612')
    return render_template('tempDT.html', filteredData=filteredData)

# Retorna a umidade entre 0h a 23h
@app.route('/umi_hora')
def umidade_hora():
    datai = '2022-11-28'
    dataf = '2022-11-29'
    result = funcoes.umidade_hora(datai, dataf, 'A612')
    return render_template('umiHR.html', filteredData=result)

# Retorna a umidade entre intervalo de dias
@app.route('/umi_dia')
def umidade_dia():
    datai = '2022-10-28'
    dataf = '2022-11-30'
    filteredData = funcoes.umidade_dia(datai, dataf, 'A612')
    return render_template('umiDT.html', filteredData=filteredData)

# Retorna a precipitação entre intervalo de dias
@app.route('/prec')
def precipitacao():
    datai = '2022-10-28'
    dataf = '2022-11-30'
    filteredData = funcoes.precipitacao(datai, dataf, 'A612')
    return render_template('prec.html', filteredData=filteredData)

# Retorna a direção e a velocidade do vento entre intervalo de dias
@app.route('/rosa_vento')
def vento():
    datai = '2022-10-17'
    dataf = '2022-11-30'
    filteredData = funcoes.vento(datai, dataf, 'A612')
    return render_template('vento.html', filteredData=filteredData)

# Retorna a evapotranspiração entre intervalo de dias
@app.route('/evapo')
def evapotranspiracao():
    datai = '2022-10-17'
    dataf = '2022-11-30'
    filteredData = funcoes.evapo(datai, dataf, 'A612')
    return render_template('evapo.html', filteredData=filteredData)

if __name__ == '__main__':
    # Defina a variável de ambiente FLASK_ENV como 'development'
    os.environ['FLASK_ENV'] = 'development'
    # Habilite o modo de depuração para mensagens de erro mais detalhadas (opcional)
    app.debug = True
    app.run())
