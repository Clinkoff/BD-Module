import smtplib
from email.message import EmailMessage
import sqlite3


def buscar_email(telegram_id):
    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT email from Clientes WHERE Telegram_id = ?", (telegram_id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado[0] if resultado else None

def enviar_email_pedido(telegram_id, assunto, conteudo):
    email_cliente = buscar_email(telegram_id)
    if not email_cliente:
        print(f"Erro: Cliente {telegram_id} não tem e-mail cadastrado.")
        return

    remetente = "EMAIL_USER"
    senha = "PASSWORD_USER"

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = email_cliente
    msg.set_content(conteudo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.send_message(msg)
        print(f"E-mail enviado para {email_cliente}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")