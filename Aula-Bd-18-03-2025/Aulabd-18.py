'''
Pegue o primeiro arquivo agenda-telefonica e em seguida iremos modificá-la para que tenha duas tabelas. Uma de contatos e uma de telefones
em um relacionamento 1:M
'''

import re
import sqlite3

def conectar_contatos(): # realizando a conexão com o banco de dados para poder salvar os dadossssss
    conexao = sqlite3.connect("agenda-de-contatos.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telefone (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefone TEXT UNIQUE NOT NULL,
            contato_id INTEGER,
            FOREIGN KEY (contato_id) REFERENCES contatos(id) ON DELETE CASCADE
        )
    ''');
    conexao.commit()
    return conexao, cursor;


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
        try:
            cursor.execute("INSERT INTO contatos (nome) VALUES (?)", (nome,)) 
            contato_id = cursor.lastrowid

            if contato_id:
                cursor.execute("INSERT INTO telefone (telefone, contato_id) VALUES (?, ?)", (telefone_formatado, contato_id))
#o insert into salva o dados - no canso, insere eles, né?

            else:
                print('error')

            conexao.commit()
            print('\nContato adicionado com sucesso!')
            break

        except sqlite3.IntegrityError:
            print('\nNome já salvo na agenda')
            break

def listar_contatos(cursor):
    cursor.execute("SELECT contatos.id, contatos.nome, telefone.telefone FROM contatos LEFT JOIN telefone ON contatos.id = telefone.contato_id")

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

def menu():
    conexao, cursor = conectar_contatos()
    while True:
        print('=' * 50)
        print('AGENDA DE CONTATOS'.center(50))
        print('=' * 50)
        print('\n1 - Adicionar novo contato')
        print('2 - Listar contatos salvos')
        print('0 - Sair da agenda')
        
        decisao = input('- ')
        if decisao == '1':
            add_contato(conexao, cursor)
        elif decisao == '2':
            listar_contatos(cursor)
        elif decisao == '5':
            print('Saindo da aplicação')
            conexao.close()
            break
        else:
            print('Opção inválida, tente novamente.')

menu()