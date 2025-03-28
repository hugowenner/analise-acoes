# main.py

from analise_acao import AnalisadorAcoes

if __name__ == "__main__":
    # Lista de ações a serem analisadas (mais de 50 ações)
    acoes = [
        'PETR4.SA', 'ITUB4.SA', 'BBDC4.SA', 'VALE3.SA', 'BBAS3.SA', 'ABEV3.SA', 'MGLU3.SA',
        'B3SA3.SA', 'WEGE3.SA', 'RADL3.SA', 'RENT3.SA', 'HAPV3.SA', 'GGBR4.SA', 'CSNA3.SA',
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BRK-B', 'V',
        'JNJ', 'PG', 'DIS', 'XOM', 'CVX', 'KO', 'PEP', 'MCD', 'INTC', 'CSCO',
        'SPY', 'QQQ', 'DIA', 'IVV', 'VTI', 'VOO', 'ARKK', 'XLK', 'XLF', 'XLE',
        'BMW.DE', 'DAI.DE', 'SAP.DE', 'HSBA.L', 'BABA', 'TCEHY', 'TSM', 'NIO', 'JD', 'SONY',
        'BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD', 'SOL-USD', 'DOT-USD', 'DOGE-USD',
        'MATIC-USD', 'LTC-USD', 'SHIB-USD', 'AVAX-USD', 'LINK-USD', 'XLM-USD', 'UNI-USD', 'ALGO-USD',
        'TRX-USD', 'NEO-USD', 'XTZ-USD', 'MKR-USD', 'AAVE-USD', 'YFI-USD', 'COMP-USD', 'CRV-USD',
        'SUSHI-USD', 'KSM-USD', 'FIL-USD', 'RUNE-USD', 'EGLD-USD', 'KAVA-USD'
    ]
    
    # Inicializa a tabela do banco de dados (se ainda não foi criada)
    analise = AnalisadorAcoes("PETR4.SA")  # Inicializa com qualquer ação
    analise.criar_tabela()
    
    # Executa a análise para todas as ações da lista
    for acao in acoes:
        print("\n" + "="*50)
        analise = AnalisadorAcoes(acao)
        analise.executar_analise()
        print("="*50)

