import sqlite3

conexao = sqlite3.connect("arquivo.db")
cursor = conexao.cursor()

def listar_livro_autor(cursor):
    cursor.execute('''
    SELECT Livros.Titulo, Autores.Nome
    FROM Livros
    JOIN Autores ON Livros.AutorID = Autores.id
''')


    Livros = cursor.fetchall()
    
    if not Livros:
        print('\nNenhuma informação salva...')
        return
    
    print('=' * 50)
    print('Autores e Livros'.center(50))
    print('=' * 50)
    for livro, autor in Livros:
        print(f'\nAutor: {autor}')
        print(f'Livro: {livro}\n')

def menu():
    while True:
        print('=' * 50)
        print('Menu de Gerência'.center(50))
        print('=' * 50)
        print('\n1 - Listar autores salvos')
        print('0 - Sair do sistema')
        
        decisao = input('- ')
        if decisao == '1':
            listar_livro_autor(cursor)
        elif decisao == '0':
            print('Saindo da aplicação...')
            conexao.close()
            break
        else:
            print('Opção inválida, tente novamente.')

menu()
