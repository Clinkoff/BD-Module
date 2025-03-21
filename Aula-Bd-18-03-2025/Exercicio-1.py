'''
1. Crie um banco de dados de uma biblioteca.
2. Criar as tabelas Livros e Autores com um relacionamento N:N usando uma tabela intermediária
LivroAutor.
3. Insira dados nas tabelas

'''


import sqlite3
from validacoes import validar_isbn

def conectar_dados(): 
    conexao = sqlite3.connect("biblioteca.bd")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            idade INTEGER NOT NULL,
            genero TEXT NOT NULL
            
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            ISBN INTEGER UNIQUE NOT NULL,
            genero TEXT NOT NULL
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autor_livro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor_id,
            livro_id,
            FOREIGN KEY (autor_id) REFERENCES autor(id) ON DELETE CASCADE,
            FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE CASCADE
        )
    ''');

    conexao.commit()
    return conexao, cursor;

def inserir_dados(conexao, cursor):

    nome_autor = input('Digite o nome do(a) autor(a): ')
    idade = int(input('Digite a idade do(a) autor(a): '))
    genero_autor = input('Autor feminino ou masculino: ')


    nome_livro = input('Digite o nome do livro: ')
    while True:
        try:
            isbn = input('Digite o código ISBN do livro: ')
            if validar_isbn(isbn):
                break

            else:
                print('Código inválido, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')
            
        
    genero_livro = input('Digite o genero do livro: ')


    while True:
        try:
            cursor.execute("INSERT INTO autor (nome, idade, genero) VALUES (?, ?, ?)", (nome_autor, idade, genero_autor,)) 
            autor_id = cursor.lastrowid

            cursor.execute("INSERT INTO livros (nome, isbn, genero) VALUES (?, ?, ?)", (nome_livro, isbn, genero_livro,))
            livro_id = cursor.lastrowid

            cursor.execute("INSERT INTO autor_livro (autor_id, livro_id) VALUES (?, ?)", (autor_id, livro_id,))
        
            conexao.commit()
            print('\nadicionados com sucesso')
            break

        except sqlite3.IntegrityError:
            print('\nInformações já adicionadas.')
            break


def listar_livro_autor(cursor):
    cursor.execute('''
    SELECT livros.nome, autor.nome
    FROM autor_livro
    JOIN livros ON autor_livro.livro_id = livro_id
    JOIN autor ON autor_livro.autor_id = autor_id
    
    ''')

    autor_livro = cursor.fetchall()
    
    if not autor_livro:
        print('\nNenhuma informação salva...')
        return
    
    print('=' * 50)
    print('Autores e Livros'.center(50))
    print('=' * 50)
    for autor in autor_livro:
        print(f'\nAutor: {autor[1]}')
        print(f'Livro: {autor[0]}\n')


def menu():
    conexao, cursor = conectar_dados()
    while True:
        print('=' * 50)
        print('Menu de gerencia'.center(50))
        print('=' * 50)
        print('\n1 - Adicionar novo livro e autor')
        print('2 - Listar autores salvos')
        print('0 - Sair do sistema')
        
        decisao = input('- ')
        if decisao == '1':
            inserir_dados(conexao, cursor)
        elif decisao == '2':
            listar_livro_autor(cursor)
        elif decisao == '5':
            print('Saindo da aplicação')
            conexao.close()
            break
        else:
            print('Opção inválida, tente novamente.')

menu()