import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    conexao.commit()
    return conexao, cursor

def cadastrar_prato(conexao, cursor):
    nome = input('Digite o nome do prato: ')
    preco = float(input('Digite o preço do prato: '))
    
    try:
        cursor.execute("INSERT INTO pratos (nome, preco) VALUES (?, ?)", (nome, preco))
        conexao.commit()
        print('Prato cadastrado com sucesso!')
    except sqlite3.IntegrityError:
        print('Prato já cadastrado.')

def atualizar_preco(conexao, cursor):
    nome = input('Digite o nome do prato que deseja atualizar: ')
    novo_preco = float(input('Digite o novo preço: '))
    
    cursor.execute("UPDATE pratos SET preco = ? WHERE nome = ?", (novo_preco, nome))
    conexao.commit()
    print('Preço atualizado com sucesso!')

def menu_pratos():
    conexao, cursor = conectar_banco()
    while True:
        print('1 - Cadastrar Prato')
        print('2 - Atualizar Preço')
        print('0 - Sair')
        decisao = input('- ')
        if decisao == '1':
            cadastrar_prato(conexao, cursor)
        elif decisao == '2':
            atualizar_preco(conexao, cursor)
        elif decisao == '0':
            conexao.close()
            break
        else:
            print('Opção inválida.')

menu_pratos()