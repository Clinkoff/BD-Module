'''
1. Criar um banco de dados chamado "loja.db".
2. Criar as tabelas Clientes, Produtos e Pedidos.
    a. Cada pedido é feito por um cliente, mas um cliente pode fazer vários pedidos. (1:M)
    b. Um pedido pode conter vários produtos, e um produto pode estar contido em vários pedidos (N:M)
3. Insira dados nas tabelas

'''


import sqlite3
from validacoes import validar_cpf, validar_data_nascimento, validar_email, validar_telefone, validar_cep

def conectar_banco(): 
    conexao = sqlite3.connect("loja.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT UNIQUE NOT NULL,
            Idade INTEGER NOT NULL,
            DataNascimento TEXT NOT NULL,
            Email TEXT NOT NULL,
            Telefone INTEGER NOT NULL,
            CPF INTEGER NOT NULL,
            CEP INTEGER NOT NULL,
            Genero TEXT NOT NULL
            
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT UNIQUE NOT NULL,
            Descricao TEXT NOT NULL,
            Preco REAL NOT NULL,
            Marca TEXT NOT NULL
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Clientes_id INTEGER NOT NULL,
            DataPedido TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Clientes_id) REFERENCES Clientes(id) ON DELETE CASCADE
        )
    ''');


    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS PedidoCompras(
            Pedidos_id INTEGER,
            Produtos_id INTEGER,
            Quantidade INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (Pedidos_id, Produtos_id),
            FOREIGN KEY (Pedidos_id) REFERENCES Pedidos(id) ON DELETE CASCADE,
            FOREIGN KEY (Produtos_id) REFERENCES Produtos(id) ON DELETE CASCADE
        );

    ''')

    conexao.commit()
    return conexao, cursor;


def inserir_dados(conexao, cursor):

    nome_cliente = input('Digite seu nome: ')
    idade = int(input('Digite sua idade: '))
    while True:
        try:
            data_nascimento = input('Digite sua data de nascimento: ')
            if validar_data_nascimento(data_nascimento):
                break

            else:
                print('Data de nascimento inválida, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')

    while True:
        try:
            email = input('Digite o seu melhor e-mail: ')
            if validar_email(email):
                break

            else:
                print('E-mail inválido, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')

    while True:
        try:
            telefone = input('Digite seu número de telefone: ')
            if validar_telefone(telefone):
                break

            else:
                print('Telefone inválido, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')

    while True:
        try:
            cpf = input('Digite o seu CPF: ')
            if validar_cpf(cpf):
                break

            else:
                print('CPF inválido, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')

    while True:
        try:
            cep = input('Digite seu CEP (somente números): ')
            if validar_cep(cep):
                break
            else: print('CEP inválido, tente novamente...')
        except Exception as e:
            print(f'Erro: {e}. Tente novamente...')

    genero = input('Feminino ou Masculino: ')
            
    nome_produto = input('Digite o nome do produto: ')
    descricao = input('Digite a descrição do produto: ')
    preco = float(input('Digite o preço do produto: '))
    marca = input('Digite a marca do produto: ')

    while True:
        try:
            cursor.execute("INSERT INTO Clientes (Nome, Idade, DataNascimento, Email, Telefone, CPF, CEP, Genero) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nome_cliente, idade, data_nascimento, email, telefone, cpf, cep, genero,)) 
            Clientes_id = cursor.lastrowid

            cursor.execute("INSERT INTO Produtos (Nome, Descricao, Preco, Marca) VALUES (?, ?, ?, ?)", (nome_produto, descricao, preco, marca,))
            Produtos_id = cursor.lastrowid

            cursor.execute("INSERT INTO Pedidos (Clientes_id) VALUES (?)", (Clientes_id,))

            Pedidos_id = cursor.lastrowid

            quantidade = int(input('Digite a quantidade do produto'))
            cursor.execute("INSERT INTO PedidoCompras (Pedidos_id, Produtos_id, Quantidade) vALUES (?, ?, ?)", (Pedidos_id, Produtos_id, quantidade,))

        
            conexao.commit()
            print('\nAdicionado com sucesso')
            break

        except sqlite3.IntegrityError:
            print('\nInformações já adicionadas.')
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")


def remover_pedido(conexao, cursor):
    Pedidos_id = input('Digite o ID do pedido que deseja cancelar: ')
    cursor.execute("DELETE FROM Pedidos WHERE id = ?", (Pedidos_id,)) #seguindo a lógica, aqui deve remover o aluno pelo id
    conexao.commit()
    print('\nPedido cancelado....')

def menu():
    conexao, cursor = conectar_banco()
    while True:
        print('=' * 50)
        print('Menu de gerenciamento'.center(50))
        print('=' * 50)
        print('\n1 - Realizar cadastro')
        print('2 - Remover aluno(a) do sistema')
        print('0 - Sair do sistema')
        
        decisao = int(input('- '))
        if decisao == 1:
            inserir_dados(conexao, cursor)
        elif decisao == 2:
            remover_pedido(conexao, cursor)
        elif decisao == 0:
            print('Saindo do site')
            conexao.close()
            break
        else:
            print('Opção inválida, tente novamente.')

menu()