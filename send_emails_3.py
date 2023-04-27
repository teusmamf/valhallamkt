import smtplib
import csv

# Configurações de conexão com o servidor SMTP
smtp_server = 'smtp.gmail.com' # exemplo para Gmail, você pode alterar para seu servidor SMTP
smtp_port = 587
smtp_username = 'martinsmateus382@gmail.com'
smtp_password = 'Ma*26042004'

# Ler o arquivo CSV com a lista de endereços de e-mail
with open('lista_de_emails.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # pula a primeira linha do arquivo CSV (cabeçalho)
    for row in reader:
        email_destino = row[0] # a primeira coluna contém os endereços de e-mail
        
        # Configurar a mensagem de e-mail
        assunto = 'Assunto'
        corpo = 'testes'
        mensagem = f'Subject: {assunto}\n\n{corpo}'
        
        # Conectar-se ao servidor SMTP e fazer login
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(smtp_username, smtp_password)
        
        # Enviar o e-mail
        server.sendmail(smtp_username, email_destino, mensagem)
        
        # Fechar a conexão com o servidor SMTP
        server.quit()
