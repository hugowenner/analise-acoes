import sqlite3
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class AnalisadorAcoes:
    def __init__(self, simbolo, periodo=1500):
        """
        Inicializa o analisador de ações
        
        :param simbolo: Símbolo da ação ou cripto (ex: 'PETR4.SA', 'BTC-USD')
        :param periodo: Período de análise em dias
        """
        self.simbolo = simbolo
        self.periodo = periodo

    def conectar_banco(self):
        """
        Conecta ao banco de dados SQLite (ou cria o banco se não existir)
        """
        conn = sqlite3.connect('analise_acoes.db')
        return conn

    def criar_tabela(self):
        """
        Cria a tabela no banco de dados, se ainda não existir
        """
        conn = self.conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analise_acoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simbolo TEXT,
                data TEXT,
                preco REAL,
                ma50 REAL,
                ma100 REAL,
                ma200 REAL,
                rsi REAL,
                recomendacao TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def obter_dados_acao(self):
        """
        Obtém dados históricos da ação ou criptomoeda
        """
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=self.periodo)
        
        try:
            # Baixa dados históricos
            acao = yf.Ticker(self.simbolo)
            dados = acao.history(
                start=data_inicio, 
                end=data_fim
            )
            
            return dados
        except Exception as e:
            print(f"Erro ao obter dados: {e}")
            return None

    def calcular_indicadores(self, dados):
        """
        Calcula indicadores técnicos para análise
        """
        # Médias móveis de 50, 100 e 200 dias
        dados['MA50'] = dados['Close'].rolling(window=50).mean()
        dados['MA100'] = dados['Close'].rolling(window=100).mean()
        dados['MA200'] = dados['Close'].rolling(window=200).mean()
        
        # Índice de Força Relativa (RSI)
        delta = dados['Close'].diff()
        
        # Ganhos e perdas
        ganhos = delta.clip(lower=0)
        perdas = -delta.clip(upper=0)
        
        # Média móvel de ganhos e perdas
        avg_ganhos = ganhos.rolling(window=14).mean()
        avg_perdas = perdas.rolling(window=14).mean()
        
        # Calcula RSI
        rs = avg_ganhos / avg_perdas
        dados['RSI'] = 100.0 - (100.0 / (1.0 + rs))
        
        return dados

    def recomendar_compra(self, dados):
        """
        Analisa os dados e recomenda compra
        """
        # Pega o último registro
        ultimo = dados.iloc[-1]
        
        # Critérios de análise
        condicoes = {
            'MA50_MA100': ultimo['MA50'] > ultimo['MA100'],
            'MA100_MA200': ultimo['MA100'] > ultimo['MA200'],
            'RSI_baixo': ultimo['RSI'] < 30,
            'tendencia_alta': ultimo['Close'] > ultimo['MA200']
        }
        
        # Pontuação de compra
        pontuacao = sum(condicoes.values())
        
        # Classificação da recomendação
        if pontuacao >= 3:
            return "COMPRAR", pontuacao
        elif pontuacao == 2:
            return "OBSERVAR", pontuacao
        else:
            return "NÃO COMPRAR", pontuacao

    def plotar_grafico(self, dados):
        """
        Plota gráfico de preços e indicadores
        """
        plt.figure(figsize=(12,6))
        plt.plot(dados.index, dados['Close'], label='Preço de Fechamento')
        plt.plot(dados.index, dados['MA50'], label='Média Móvel 50 dias')
        plt.plot(dados.index, dados['MA100'], label='Média Móvel 100 dias')
        plt.plot(dados.index, dados['MA200'], label='Média Móvel 200 dias')
        plt.title(f'Análise de Ações - {self.simbolo}')
        plt.xlabel('Data')
        plt.ylabel('Preço')
        plt.legend()
        plt.show()

    def salvar_dados_banco(self, dados, recomendacao):
        """
        Salva os dados da análise no banco de dados
        """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        for i, row in dados.iterrows():
            # Converte a data para string no formato 'YYYY-MM-DD'
            data_str = row.name.strftime('%Y-%m-%d')

            cursor.execute('''
                INSERT INTO analise_acoes (simbolo, data, preco, ma50, ma100, ma200, rsi, recomendacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.simbolo,
                data_str,  # A data foi convertida para string
                row['Close'],
                row['MA50'],
                row['MA100'],
                row['MA200'],
                row['RSI'],
                recomendacao
            ))

        conn.commit()
        conn.close()

    def executar_analise(self):
        """
        Método principal para executar análise completa
        """
        # Obtém dados
        dados = self.obter_dados_acao()
        
        if dados is not None:
            # Calcula indicadores
            dados_analisados = self.calcular_indicadores(dados)
            
            # Recomendação de compra
            recomendacao, pontuacao = self.recomendar_compra(dados_analisados)
            
            # Resultados
            print(f"Símbolo: {self.simbolo}")
            print(f"Último Preço: R$ {dados_analisados['Close'].iloc[-1]:.2f}")
            print(f"Recomendação: {recomendacao}")
            print(f"Pontuação: {pontuacao}/4")
            
            # Plota gráfico
            self.plotar_grafico(dados_analisados)

            # Salva os dados no banco de dados
            self.salvar_dados_banco(dados_analisados, recomendacao)
            
            return recomendacao

# Exemplo de uso
if __name__ == "__main__":
    # Lista de ações a serem analisadas
    acoes = [
        'PETR4.SA', 'ITUB4.SA', 'BBDC4.SA', 'VALE3.SA', 'BBAS3.SA', 'ABEV3.SA', 'MGLU3.SA',
        'B3SA3.SA', 'WEGE3.SA', 'RADL3.SA', 'RENT3.SA', 'HAPV3.SA', 'GGBR4.SA', 'CSNA3.SA',
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BRK-B', 'V',
        'JNJ', 'PG', 'DIS', 'XOM', 'CVX', 'KO', 'PEP', 'MCD', 'INTC', 'CSCO'
    ]
    
    for acao in acoes:
        print("\n" + "="*50)
        analise = AnalisadorAcoes(acao)
        analise.executar_analise()
        print("="*50)
