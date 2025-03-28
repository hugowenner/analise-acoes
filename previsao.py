import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def prever_precos(simbolo, dias=7):
    """
    Faz uma previsão simples dos preços futuros usando regressão linear.
    
    :param simbolo: Símbolo da ação (ex: 'AAPL', 'PETR4.SA')
    :param dias: Número de dias para prever
    :return: DataFrame com as previsões
    """
    # Baixar dados históricos
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=365)  # Último ano de dados
    acao = yf.Ticker(simbolo)
    dados = acao.history(start=data_inicio, end=data_fim)

    if dados.empty:
        return None

    # Criar variável de tempo
    dados['Dias'] = np.arange(len(dados))

    # Treinar modelo de regressão linear
    modelo = LinearRegression()
    modelo.fit(dados[['Dias']], dados['Close'])

    # Fazer previsões para os próximos dias
    dias_futuros = np.arange(len(dados), len(dados) + dias).reshape(-1, 1)
    previsoes = modelo.predict(dias_futuros)

    # Criar DataFrame com as previsões
    datas_futuras = [data_fim + timedelta(days=i) for i in range(1, dias + 1)]
    df_previsoes = pd.DataFrame({
        'Data': datas_futuras,
        'Previsao': previsoes
    })  # <- Correção aqui: fechamento correto das chaves {}

    return df_previsoes
