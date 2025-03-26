import sqlite3



def conectar_banco(): 
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Serve INT NOT NULL,
            Preco REAL NOT NULL,
            Descricao TEXT NOT NULL
            
            
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT UNIQUE NOT NULL, 
            DataNascimento TEXT NOT NULL, 
            CPF INTEGER UNIQUE NOT NULL,
            Email TEXT NOT NULL, 
            Telefone INTEGER NOT NULL
        )
    ''');


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Clientes_id INTEGER, 
            
            
            
        )
    ''');

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS ClientePedido(
            Pedidos_id INTEGER,
            Clientes_id INTEGER,
            PRIMARY KEY (Pedidos_id, Clientes_id),
            FOREIGN KEY (Pedidos_id) REFERENCES Pedidos(id) ON DELETE CASCADE,
            FOREIGN KEY (Clientes_id) REFERENCES Clientes(id) ON DELETE CASCADE
        )

    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Avaliacoes(
            Clientes_id INTEGER,
            
        )

    ''')


    conexao.commit()
    return conexao, cursor;



def cadastrar_pratos(conexao, cursor):


    nome_prato  = input('Digite o nome do prato: ')




