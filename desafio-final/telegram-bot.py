from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import sqlite3
import os
from dotenv import  load_dotenv

load_dotenv()

bot_token = os.getenv("TOKEN_BOT")

def start(update: Update, Context: CallbackContext):
    update.message.reply_text("Bem vindo ao restaurante Cyber... Utilize /cardapio para ver os pratos disponiveis")

def cardapio(update: Update, context: CallbackContext):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, Nome, Preco FROM Pratos")
    pratos = cursor.fetchall()
    conexao.close()

    menu = "\n".join([f"{pratos[0]}. {pratos[1]} - R$ {pratos[2]:.2f}"for prato in pratos])
    update.message.reply_text(f"Cardápio: \n{menu}\n\nPara pedir, escreva: /pedir <id do prato>")

def pedir(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Use: /pedir <id do prato>")
        return
    
    prato_id = context.args[0]
    cliente = update.message.chat.username

    coenxao = sqlite3.connect("restaurante.db")
    cursor = coenxao.cursor()
    cursor.execute("INSERT INTO Pedidos (Cliente_telegram, Prato_id) VALUES (?,?)", (cliente, prato_id))
    coenxao.commit()
    coenxao.close()

    update.message.reply_text("Pedido realizado com sucesso. utiliza /status para acompanhar seu pedido")

def status(update: Update, context: CallbackContext):
    cliente = update.message.chat.username

    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT Status FROM Pedidos WHERE Cliente_telegram = ? ORDER BY id DESC LIMIT 1", (cliente,))
    pedido = cursor.fetchone()
    conexao.close()

    if pedido:
        update.message.reply_text(f'Status do seu pedido: {pedido[0]}')
    else:
        update.message.reply_text("Você não tem pedidos em andamento")

def avaliar(update: Update, context: CallbackContext):
    if len(context.args[0]) < 2:
        update.message.reply_text("Use: /avaliar <nota de 1 a 5> <comentário>")
        return
    
    nota = int(context.args[0])
    comentario = " ".join(context.args[1:])
    cliente = update.message.chat.username
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO Avaliacoes (Cliente_telegram, Nota, Comentario) VALUES (?, ?, ?)", (cliente, nota, comentario))
    conexao.commit()
    conexao.close()
    update.message.reply_text("Obrigado pela sua avaliação..")

def main():
    Updater = Updater(bot_token, use_context = True)
    dp = Updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cardapio", cardapio))
    dp.add_handler(CommandHandler("pedir", pedir))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("avaliar", avaliar))

    Updater.start_polling()
    Updater.idle()

if __name__ == "__main__":
    main()