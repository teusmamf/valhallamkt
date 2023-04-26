from google.oauth2 import flow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

import base64
from email.mime.text import MIMEText
import os

# Configure o ID do cliente OAuth do Google
CLIENT_ID = '763300706855-nv8lh5282ru404dep4esopkplfim8gu2.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPE = ['https://www.googleapis.com/auth/gmail.send']
REDIRECT_URI = 'http://localhost:8000/'

# Construa o objeto Flow
flow = flow.Flow.from_client_config(
    client_config={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE
    },
    redirect_uri=REDIRECT_URI
)

# Obtenha a URL de autorização
auth_url, _ = flow.authorization_url(prompt='consent')

# Imprima a URL de autorização e peça ao usuário que acesse ela em um navegador
print('Por favor, acesse esta URL e faça login: \n{}'.format(auth_url))

# Depois que o usuário der permissão, eles serão redirecionados para a URL REDIRECT_URI.
# A URL terá um parâmetro de consulta "code".
code = input('Digite o código de autorização: ')

# Troque o código de autorização pela credencial de acesso
flow.fetch_token(code=code)

# Construa a API do Gmail
creds = Credentials.from_authorized_user_info(info=flow.credentials.to_json())

service = build('gmail', 'v1', credentials=creds)

def send_email(to, subject, body):
    """Envia um email com o corpo especificado para o destinatário especificado.
    """
    try:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        
        print(F'The message was sent to {to} with email Id: {send_message["id"]}')
        
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
        
    return send_message
