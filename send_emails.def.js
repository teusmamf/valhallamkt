const {google} = require('googleapis');
const fs = require('fs');
const csv = require('csv-parser');
const nodemailer = require('nodemailer');
const data = fs.readFileSync('emailsvalhalla-aea098b4a82a.json');
const json = JSON.parse(data);
const keyFile = json.private_key;
// Autenticação do Google
const auth = new google.auth.GoogleAuth({
  
  keyFile:keyFile,
  
  scopes: ['https://www.googleapis.com/auth/gmail.send']
});

// Criação do cliente --------------||||---------------------||||
const gmail = google.gmail({version: 'v1', auth});

// Nodemailer--------------||||---------------------||||
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'martinsmateus382@gmail.com',
    pass: 'ktzoguattjmlvgut'
  }
});

// Leitura da lista--------------||||---------------------||||
fs.createReadStream('lista_de_emails.csv')
  .pipe(csv())
  .on('data', (row) => {
    // Para cada linha do CSV, envia um e-mail--------------||||---------------------||||
    const mailOptions = {
      from: 'martinsmateus382@gmail.com',
      to: row.email,
      subject: 'teste2',
      text: 'teste valhalla'
    };
    console.log(mailOptions.to);

    // Envia o e-mail --------------||||---------------------||||
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.error(error);
      } else {
        console.log(`E-mail enviado para ${row.email}: ${info.response}`);
        
        //enviado--------------||||---------------------||||
        gmail.users.messages.modify({
          userId: 'me',
          id: info.messageId,
          requestBody: {
            removeLabelIds: ['UNREAD']
          }
        }, (err, res) => {
          if (err) {
            console.error(err);
          } else {
            console.log(`E-mail marcado como enviado: ${res.data.id}`);
          }
        });
      }
    });
  })
  .on('end', () => {
    console.log('Todos os e-mails foram enviados!');
  });
