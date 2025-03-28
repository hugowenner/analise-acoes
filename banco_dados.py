import sqlite3

def criar_tabela():
    """Cria a tabela se não existir"""
    conexao = sqlite3.connect("analise_acoes.db")
    cursor = conexao.cursor()
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
    conexao.commit()
    conexao.close()

def salvar_dados_banco(simbolo, recomendacao):
    """Salva os dados no banco"""
    conexao = sqlite3.connect("analise_acoes.db")
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO analise_acoes (simbolo, data, preco, recomendacao)
        VALUES (?, datetime('now'), NULL, ?)
    ''', (simbolo, recomendacao))
    conexao.commit()
    conexao.close()
