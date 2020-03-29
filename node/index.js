// replace all 
String.prototype.replaceAll = function(str1, str2, ignore) {
  return this.replace(
    new RegExp(
      str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g, '\\$&'),
      ignore ? 'gi' : 'g'
    ),
    typeof str2 == 'string' ? str2.replace(/\$/g, '$$$$') : str2
  );
};
const mailerOpt = require('./secrets');
const fs = require('fs');
const nodemailer = require('nodemailer');
let html = '';
fs.readFile('posts.dat', 'utf8', function(err, contents) {
  const posts = contents.split(' ');
  for (let post of posts) {
    post = post.split('?');
    html = html + `<p><a href="${post[1]}">${post[0].replaceAll('_', ' ')}</a></p><br>`;
  }
  const smtpTrans = nodemailer.createTransport(
      `smtps://${mailerOpt.sender}:` +
      encodeURIComponent(mailerOpt.passwd) +
      '@smtp.gmail.com:465'
  );
  //Mail options
  const mailOpts = {
    from: 'Reddit dhia cron',
    to: mailerOpt.receiver,
    subject: 'Daily custom reddit notifications for you Mr dhia',
    html
  };
    smtpTrans.sendMail(mailOpts, function(error, response) {
      //Alert on event of message sent succeeds or fail.
      if (error) {
        console.log('[ERROR]: Error while notifying Mr dhia about the new user!', error);
        console.log('====================================');
        smtpTrans.close();
      }
      console.log('response: ', response);
      console.log('[INFO]: Mr.Dhia is notified');
      console.log('====================================');
      smtpTrans.close();
    });
});
