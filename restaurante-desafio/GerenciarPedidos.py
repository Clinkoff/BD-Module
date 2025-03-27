from Cadastrar import conectar_banco


def gerenciar_pedidos(conexao, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prato_id INTEGER,
            status TEXT NOT NULL,
            FOREIGN KEY (prato_id) REFERENCES pratos(id)
        )
    ''')
    conexao.commit()

def criar_pedido(conexao, cursor):
    cursor.execute("SELECT * FROM pratos")
    pratos = cursor.fetchall()
    
    print("Pratos disponíveis:")
    for prato in pratos:
        print(f'ID: {prato[0]}, Nome: {prato[1]}, Preço: {prato[2]}')
    
    prato_id = int(input('Digite o ID do prato que deseja pedir: '))
    cursor.execute("INSERT INTO pedidos (prato_id, status) VALUES (?, 'em preparo')", (prato_id,))
    conexao.commit()
    print('Pedido criado com sucesso!')

def atualizar_status_pedido(conexao, cursor):
    pedido_id = int(input('Digite o ID do pedido que deseja atualizar: '))
    novo_status = input('Digite o novo status (em preparo, pronto, entregue): ')
    
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    conexao.commit()
    print('Status atualizado com sucesso!')

def menu_pedidos():
    conexao, cursor = conectar_banco()
    gerenciar_pedidos(conexao, cursor)
    
    while True:
        print('1 - Criar Pedido')
        print('2 - Atualizar Status do Pedido')
        print('0 - Sair')
        decisao = input('- ')
        if decisao == '1':
            criar_pedido(conexao, cursor)
        elif decisao == '2':
            atualizar_status_pedido(conexao, cursor)
        elif decisao == '0':
            conexao.close()
            break
        else:
            print('Opção inválida.')

menu_pedidos()