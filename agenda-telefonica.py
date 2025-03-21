'''
refazer o sistema de gerenciamento de agenda telefonica, só que ao invés de salvar os dados em um arquivo .json, salvar diretamente no banco de dados
'''
import sqlite3
import re

def conectar_banco(): # realizando a conexão com o banco de dados para poder salvar os dadossssss
    conexao = sqlite3.connect("agenda-telefonica.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conexao.commit()
    return conexao, cursor

def validar_telefone(telefone):
    numeros = re.sub(r'\D', '', telefone)
    if len(numeros) == 11:
        return f'({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}'
    elif len(numeros) == 10:
        return f'({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}'
    else:
        return telefone

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def add_contato(conexao, cursor):
    nome = input('Digite o nome do contato: ').strip()
    telefone = input('Digite o número de telefone do contato: ')
    telefone_formatado = validar_telefone(telefone)
    
    while True:
        email = input('Digite o e-mail do contato: ').strip()
        if validar_email(email):
            break
        else:
            print('\nE-mail inválido, tente novamente.')
    
    try:
        cursor.execute("INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)", (nome, telefone_formatado, email)) #o insert into salva o dados - no canso, insere eles, né?
        conexao.commit()
        print('\nContato adicionado com sucesso!')
    except sqlite3.IntegrityError:
        print('\nNome já salvo na agenda')

def mod_contato(conexao, cursor):
    nome = input('Digite o nome do contato que deseja modificar: ')
    cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome,)) # O select busca o dado em especifico dentro do banco de dados 
    contato = cursor.fetchone()
    
    if not contato:
        print('\nContato não encontrado')
        return
    
    print('O que deseja mudar?\n1 - Nome\n2 - E-mail\n3 - Telefone\n4 - Cancelar')
    decisao = input('- ')
    
    if decisao == '1':
        novo_nome = input('Digite o novo nome: ').strip()
        cursor.execute("UPDATE contatos SET nome = ? WHERE nome = ?", (novo_nome, nome)) #o uptade atualiza o dado selecionado
    elif decisao == '2':
        while True:
            novo_email = input('Digite o novo e-mail do contato: ').strip()
            if validar_email(novo_email):
                cursor.execute("UPDATE contatos SET email = ? WHERE nome = ?", (novo_email, nome))
                break
            else:
                print('E-mail inválido, tente novamente.')
    elif decisao == '3':
        novo_telefone = input('Digite o novo telefone do contato: ')
        cursor.execute("UPDATE contatos SET telefone = ? WHERE nome = ?", (validar_telefone(novo_telefone), nome)) 
    elif decisao == '4':
        print('\nVoltando ao menu inicial...\n')
        return
    else:
        print('Opção inválida.')
        return
    
    conexao.commit()
    print('\nDados atualizados com sucesso!')

def remover_contato(conexao, cursor):
    nome = input('Digite o nome do contato que deseja remover: ')
    cursor.execute("DELETE FROM contatos WHERE nome = ?", (nome,)) #bem, npé o delete deleta kkkk
    conexao.commit()
    print('\nContato removido da agenda.')

def listar_contatos(cursor):
    cursor.execute("SELECT * FROM contatos") 
    contatos = cursor.fetchall()
    
    if not contatos:
        print('\nNenhum contato salvo na agenda...')
        return
    
    print('=' * 50)
    print('CONTATOS SALVOS'.center(50))
    print('=' * 50)
    for contato in contatos:
        print(f'\nID: {contato[0]}')
        print(f'Nome: {contato[1]}')
        print(f'Telefone: {contato[2]}')
        print(f'E-mail: {contato[3]}\n')

def menu():
    conexao, cursor = conectar_banco()
    while True:
        print('=' * 50)
        print('AGENDA DE CONTATOS'.center(50))
        print('=' * 50)
        print('\n1 - Adicionar novo contato')
        print('2 - Editar um contato já existente')
        print('3 - Remover um contato')
        print('4 - Listar contatos salvos')
        print('5 - Sair da agenda')
        
        decisao = input('- ')
        if decisao == '1':
            add_contato(conexao, cursor)
        elif decisao == '2':
            mod_contato(conexao, cursor)
        elif decisao == '3':
            remover_contato(conexao, cursor)
        elif decisao == '4':
            listar_contatos(cursor)
        elif decisao == '5':
            print('Saindo da aplicação')
            conexao.close()
            break
        else:
            print('Opção inválida, tente novamente.')

menu()