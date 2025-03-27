from Cadastrar import conectar_banco


def relatorio_vendas(conexao, cursor):
    cursor.execute('''
        SELECT pratos.nome, COUNT(pedidos.id) AS total_vendas
        FROM pedidos
        JOIN pratos ON pedidos.prato_id = pratos.id
        GROUP BY pratos.nome
    ''')
    vendas = cursor.fetchall()
    
    print('Relatório de Vendas:')
    for prato, total in vendas:
        print(f'Prato: {prato}, Total Vendido: {total}')

def menu_relatorios():
    conexao, cursor = conectar_banco()
    while True:
        print('1 - Emitir Relatório de Vendas')
        print('0 - Sair')
        decisao = input('- ')
        if decisao == '1':
            relatorio_vendas(conexao, cursor)
        elif decisao == '0':
            conexao.close()
            break
        else:
            print('Opção inválida.')

menu_relatorios()