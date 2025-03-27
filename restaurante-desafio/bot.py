from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Função para iniciar o bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Eu sou o bot do restaurante. Como posso ajudar?')

# Função para responder a mensagens
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Você disse: {update.message.text}')

def main():
    # Substitua 'YOUR_TOKEN' pelo token do seu bot
    updater = Updater("YOUR_TOKEN")

    # Obtenha o dispatcher para registrar os manipuladores
    dispatcher = updater.dispatcher

    # Comandos
    dispatcher.add_handler(CommandHandler("start", start))

    # Responder a mensagens
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Iniciar o bot
    updater.start_polling()

    # Executar até que o usuário pressione Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()