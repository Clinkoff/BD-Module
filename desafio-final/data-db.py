import sqlite3
from validacoes import validar_email

def criar_banco():
    conexao = sqlite3.connect("restaurante.bd")
    cursor = conexao.cursor()


    # pratos

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pratos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TXT NOT NULL,
        Preco REAL NOT NULL,
        Serve TEXT NOT NULL
    )
    """)

    # Pedidos

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pedidos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente_telegram TEXT NOT NULL,
        Prato_id INTEGER,
        Status TEXT DEFAULT 'Em preparo',
        FOREIGN KEY (Prato_id) REFERENCES Prato(id)
    )
    """)

    # Tabela clientes

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clientes(
        Telegram_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Email TEXT NOT NULL
    )
    """)

    # tabela de avalição

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Avaliacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Cliente_telegram TEXT NOT NULL,
        Nota INTEGER CHECK (Nota >= 1 AND Nota <= 5),
        Comentario TEXT
    )
    """)
    conexao.commit()
    return conexao, cursor;


# seção gestor

def cadastrador_pratos(Nome, Preco):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO Pratos (Nome, Preco) VALUES (?, ?)", (Nome, Preco))
    conexao.commit()
    conexao.close()

def upate_precos(Prato_id, novo_preco):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE Pratos SET Preco = ? WHERE id = ?", (novo_preco, Prato_id))
    conexao.commit()
    conexao.close()

def update_pedido_status(Pedido_id, Novo_satus):
    conexao = sqlite3("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE Pedidos SET Status = ? WHERE id = ?", (Novo_satus, Pedido_id))
    conexao.commit()
    conexao.close()

def relatorio_vendas():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT Pratos.Nome, COUNT (Pedidos.id) AS Total_vendas
        FROM Pedidos
        JOIN Pratos ON Pedidos.Prato_id = Pratos_id
        WHERE Status = 'Entregue'
        GROUP BY Pratos.Nome
    """)
    vendas = cursor.fetchall()
    conexao.close()

    print('\nRelatório de vendas')
    for prato, total in vendas:
        print(f'{prato}: {total} vendas')