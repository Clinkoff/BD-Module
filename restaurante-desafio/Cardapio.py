import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Função para conectar ao banco de dados
def conectar_banco():
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    return conexao, cursor

# Função para ver o cardápio
def ver_cardapio(update: Update, context: CallbackContext) -> None:
    conexao, cursor = conectar_banco()
    cursor.execute("SELECT id, nome, preco FROM pratos")
    pratos = cursor.fetchall()
    
    if pratos:
        mensagem = "Cardápio:\n"
        for prato in pratos:
            mensagem += f"ID: {prato[0]}, Nome: {prato[1]}, Preço: R${prato[2]:.2f}\n"
    else:
        mensagem = "O cardápio está vazio."
    
    update.message.reply_text(mensagem)
    conexao.close()

# Função para fazer um pedido
def fazer_pedido(update: Update, context: CallbackContext) -> None:
    try:
        prato_id = int(context.args[0])  # O ID do prato deve ser passado como argumento
        conexao, cursor = conectar_banco()
        
        # Verificar se o prato existe
        cursor.execute("SELECT nome FROM pratos WHERE id = ?", (prato_id,))
        prato = cursor.fetchone()
        
        if prato:
            # Criar o pedido
            cursor.execute("INSERT INTO pedidos (prato_id, status) VALUES (?, 'em preparo')", (prato_id,))
            conexao.commit()
            update.message.reply_text(f"Pedido feito com sucesso! Você pediu: {prato[0]}.")
        else:
            update.message.reply_text("Prato não encontrado. Por favor, verifique o ID.")
        
        conexao.close()
    except (IndexError, ValueError):
        update.message.reply_text("Por favor, forneça o ID do prato que deseja pedir.")

def main():
    # Substitua 'YOUR_TOKEN' pelo token do seu bot
    updater = Updater("YOUR_TOKEN")

    # Obtenha o dispatcher para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Comandos
    dispatcher.add_handler(CommandHandler("cardapio", ver_cardapio))
    dispatcher.add_handler(CommandHandler("pedir", fazer_pedido))

    # Iniciar o bot
    updater.start_polling()

    # Executar até que o usuário pressione Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()