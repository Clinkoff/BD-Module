'''
1. Criar um banco de dados chamado "Escola.db".
2. Criar as tabelas Alunos, Cursos e Matriculas:
a. Alunos: ID, Nome, DataNascimento.
b. Cursos: ID, Nome, Duracao.
c. Matriculas: ID, AlunoID, CursoID, DataMatricula.
i. Adicionar chaves estrangeiras para relacionar AlunoID e CursoID.
3. Insira dados nas tabelas

'''

import re
from datetime import datetime
import sqlite3
from validacoes import validar_cpf, validar_email, validar_telefone, validar_data_nascimento


def conectar_dados(): 
    conexao = sqlite3.connect("escola.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aluno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            idade INTEGER NOT NULL,
            cpf INTEGER UNIQUE NOT NULL,
            data_nascimento TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            genero TEXT NOT NULL,
            telefone INTEGER NOT NULL
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            duracao INTEGER NOT NULL,
            tipo TEXT NOT NULL
        )
    ''');

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matriculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id,
            cursos_id,
            FOREIGN KEY (aluno_id) REFERENCES aluno(id) ON DELETE CASCADE,
            FOREIGN KEY (cursos_id) REFERENCES cursos(id) ON DELETE CASCADE
        )
    ''');

    conexao.commit()
    return conexao, cursor;

def inserir_dados(conexao, cursor):

    nome_aluno = input('Digite o nome do(a) aluno(a): ')
    idade = int(input('Digite a idade do(a) aluno(a): '))
    genero = input('aluno(a) feminino ou masculino: ')
    while True:
        try:
            cpf = input('Digite o CPF do aluno: ')
            if validar_cpf(cpf):
                break

            else:
                print('CPF inválido, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')


    while True:
        try:
            data_nascimento = input('Digite o a data de nascimento do aluno: ')
            if validar_data_nascimento(data_nascimento):
                break

            else:
                print('Data de nascimento inválida, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')

    while True:
        try:
            email = input('Digite o e-mail do aluno: ')
            if validar_email(email):
                break

            else:
                print('E-mail inválido, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')

    while True:
        try:
            telefone = input('Digite o telefone do aluno: ')
            if validar_telefone(telefone):
                break

            else:
                print('Telefone inválido, tente novamente...')

        except Exception as e:
            print(f'Erro: {e}. Tente novamente.')
            
    nome_curso = input('Digite o nome do curso: ')
    duracao = int(input('Digite o tempo de duração do curso em ANOS: '))
    tipo = input('Digite o tipo do curso(EX: bacharelado ou técnico): ')

    while True:
        try:
            cursor.execute("INSERT INTO aluno (nome, idade, cpf, data_nascimento, email, genero, telefone) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome_aluno, idade, cpf, data_nascimento, email, genero, telefone,)) 
            aluno_id = cursor.lastrowid

            cursor.execute("INSERT INTO cursos (nome, duracao, tipo) VALUES (?, ?, ?)", (nome_curso, duracao, tipo,))
            cursos_id = cursor.lastrowid

            cursor.execute("INSERT INTO matriculas (aluno_id, cursos_id) VALUES (?, ?)", (aluno_id, cursos_id,))
        
            conexao.commit()
            print('\nadicionado com sucesso')
            break

        except sqlite3.IntegrityError:
            print('\nInformações já adicionadas.')
            break


def listar_matriculas(cursor):
    cursor.execute('''
    SELECT aluno.id, 
        aluno.nome, 
        aluno.data_nascimento, 
        aluno.cpf, 
        cursos.nome 
    FROM matriculas
    JOIN aluno ON matriculas.aluno_id = aluno.id
    JOIN cursos ON matriculas.cursos_id = cursos.id
    ''')

    matriculas = cursor.fetchall()

    if not matriculas:
        print('\nNenhuma informação salva...')
        return
    
    print('=' * 50)
    print('Alunos e Cursos'.center(50))
    print('=' * 50)
    
    hoje = datetime.today()
    
    for aluno in matriculas:
        aluno_id = aluno[0]
        nome_aluno = aluno[1]
        data_nascimento = aluno[2]
        cpf = aluno[3]
        nome_curso = aluno[4]

        # aqui pra calcular a idade e mostrar sempre a atual
        try:
            # Verifica se a data está no formato correto antes de converter
            data_nasc = datetime.strptime(data_nascimento, "%d/%m/%Y")
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        except ValueError:
            print(f"Erro ao processar a data de nascimento do aluno {nome_aluno}. Valor recebido: {data_nascimento}")
            continue
        
        print(f'\nID: {aluno_id}')
        print(f'Aluno: {nome_aluno}')
        print(f'Idade: {idade} anos')
        print(f'CPF: {cpf}')
        print(f'Curso: {nome_curso}\n')




def remover_aluno(conexao, cursor):
    aluno_id = input('Digite o ID do aluno(a) que deseja remover: ')
    cursor.execute("DELETE FROM aluno WHERE id = ?", (aluno_id,)) #seguindo a lógica, aqui deve remover o aluno pelo id
    conexao.commit()
    print('\nAluno(a) removido do sistema.')

def menu():
    conexao, cursor = conectar_dados()
    while True:
        print('=' * 50)
        print('Menu de gerenciamento'.center(50))
        print('=' * 50)
        print('\n1 - Adicionar novo aluno e curso')
        print('2 - Listar alunos matriculados')
        print('3 - Remover aluno(a) do sistema')
        print('0 - Sair do sistema')
        
        decisao = int(input('- '))
        if decisao == 1:
            inserir_dados(conexao, cursor)
        elif decisao == 2:
            listar_matriculas(cursor)
        elif decisao == 3:
            remover_aluno(conexao, cursor)
        elif decisao == 0:
            print('Saindo dao sistema')
            conexao.close()
            break
        else:
            print('Opção inválida, tente novamente.')

menu()