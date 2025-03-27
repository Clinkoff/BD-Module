import sqlite3

def criar_banco():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prato_id INTEGER,
            status TEXT NOT NULL,
            FOREIGN KEY (prato_id) REFERENCES pratos(id)
        )
    ''')
    
    conexao.commit()
    conexao.close()
    print("Banco de dados 'restaurante.db' criado com sucesso!")

criar_banco()