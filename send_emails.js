const fs = require('fs');
const readline = require('readline');
const { google } = require('googleapis');
const { OAuth2Client } = require('google-auth-library');
const nodemailer = require('nodemailer');
const csv = require('csv-parser');

// Define as informações do cliente OAuth2
const CLIENT_ID = '961108638585-birkdjapfaq2jnpa16s8kb50b5ijqtir.apps.googleusercontent.com';
const CLIENT_SECRET = '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';
const REDIRECT_URI = 'http://localhost:8000';
const SENDER_EMAIL = 'martinsmateus482@gmail.com';
const SUBJECT = 'teste';
const BODY = 'teste emails valhalla';
const RECIPIENTS_CSV_PATH = 'lista_de_emails.csv';

// Define as permissões necessárias para enviar e-mails
const SCOPES = ['https://www.googleapis.com/auth/gmail.send'];

async function main() {
  try {
    // Cria o cliente OAuth2
    const oAuth2Client = new OAuth2Client(
      CLIENT_ID,
      CLIENT_SECRET,
      REDIRECT_URI,
    );

    // Checa se já existe um token de acesso salvo
    let token;
    if (fs.existsSync('token.json')) {
      token = JSON.parse(fs.readFileSync('token.json'));
      oAuth2Client.setCredentials(token);
    } else {
      // Gera a URL de autorização
      const authUrl = oAuth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES,
      });
      console.log(`Por favor, autorize o aplicativo no seguinte URL:\n${authUrl}`);

      // Lê o código de autorização do usuário
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
      });
      const code = await new Promise((resolve) => {
        rl.question('Digite o código de autorização: ', resolve);
      });
      rl.close();

      // Obtém as credenciais de acesso
      const { tokens } = await oAuth2Client.getToken(code);
      token = tokens;
      oAuth2Client.setCredentials(token);

      // Salva as credenciais de acesso em um arquivo
      fs.writeFileSync('token.json', JSON.stringify(token));
    }

    // Cria o objeto de transporte do Nodemailer
    const transport = nodemailer.createTransport({
      service: 'Gmail',
      auth: {
        type: 'OAuth2',
        user: SENDER_EMAIL,
        clientId: CLIENT_ID,
        clientSecret: CLIENT_SECRET,
        refreshToken: token.refresh_token,
        accessToken: token.access_token,
      },
    });

    // Lê a lista de destinatários do arquivo CSV
    const recipients = [];
    fs.createReadStream(RECIPIENTS_CSV_PATH)
      .pipe(csv())
      .on('data', (data) => {
        recipients.push(data.email);
      })
      .on('end', async () => {
        // Envia um e-mail para cada destinatário
        for (const recipient of recipients) {
          const message = {
            to: recipient,
            from: SENDER_EMAIL,
            subject: SUBJECT,
            text: BODY,
          };
          await transport.sendMail(message);
        }
      });
  } catch (err) {
    console.error(err);
  }
}

main();