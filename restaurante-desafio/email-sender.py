import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviar_email(destinatario, assunto, conteudo):
    message = Mail(
        from_email='seu_email@dominio.com',
        to_emails=destinatario,
        subject=assunto,
        plain_text_content=conteudo
    )
    try:
        sg = SendGridAPIClient('SUA_API_KEY')
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e.message)

def confirmar_pedido(pedido):
    # Lógica para confirmar o pedido
    # ...
    # Enviar notificação por e-mail
    enviar_email(pedido.cliente_email, 
                 'Confirmação de Pedido', 'Seu pedido foi confirmado!')