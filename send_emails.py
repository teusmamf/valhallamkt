import json
import os
import csv
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions
import smtplib




# Define as informações do cliente OAuth2

SCOPE = ['https://www.googleapis.com/auth/gmail.send']


SENDER_EMAIL = 'martinsmateus482@gmail.com'
SUBJECT = 'teste'
BODY = 'teste emails valhalla'


RECIPIENTS_CSV_PATH = 'lista_de_emails.csv'


flow = InstalledAppFlow.from_client_config({
    "web":{
            "client_id":"763300706855-voorob5g4s6nsj3085l18nssedkk36qe.apps.googleusercontent.com",
            "project_id":"psychic-cascade-338021",
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret":"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",
            "redirect_uri":"http://localhost:8000",
            "javascript_origins":["http://localhost:8000"]
            }
}, scopes=SCOPE)


creds = None
if os.path.exists('token.json'):
    with open('token.json', 'r') as token:
        creds = Credentials.from_authorized_user_info(
            info=json.load(token), scopes=SCOPE)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except google.auth.exceptions.RefreshError:
            print('Não foi possível atualizar as credenciais do usuário.')
            exit()
    else:
        auth_url, _ = flow.authorization_url(prompt='consent', redirect_uriS=["http://localhost:8000"])
        print(f'Por favor, autorize o aplicativo no seguinte URL:\n{auth_url}')
        auth_code = input('Digite o código de autorização: ')
        try:
            flow.fetch_token(code=auth_code)
            creds = flow.credentials
        except google.auth.exceptions.RefreshError:
            print('Não foi possível obter as credenciais do usuário.')
            exit()
    with open('token.json', 'w') as token:
        json.dump(creds.to_authorized_user_info(), token)
print("URL DE REDIRECIONAMENTO :",["http://localhost:8000"])
# Cria a conexão com o servidor SMTP do Google
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
except Exception as e:
    print(f'Não foi possível se conectar ao servidor SMTP: {e}')
    exit()

# Faz o login no servidor SMTP com as credenciais do usuário
try:
    server.login(SENDER_EMAIL, creds)
except smtplib.SMTPAuthenticationError:
    print('Não foi possível fazer login no servidor SMTP.')
    exit()

# Abre o arquivo CSV com a lista de destinatários
try:
    with open(RECIPIENTS_CSV_PATH, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Ignora o cabeçalho do arquivo CSV
        for row in reader:
            recipient_email = row[0]
            # Cria a mensagem de e-mail
            message = MIMEText(BODY)
            message['to'] = recipient_email
            message['from'] = SENDER_EMAIL
except Exception as e:
    print(f'Erro ao abrir o arquivo CSV: {e}')
    exit()
finally:
    csv_file.close()