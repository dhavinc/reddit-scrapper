import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_email():
    email_list = [
        secrets.RECEIVER_EMAIL
    ]
    subject = 'Hey you! I got something for you to check out...'
    # Port 587 is port to use when sending emails from an app with TLS required
    # See https://support.google.com/a/answer/176600?hl=en
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    print(secrets.SENDER_EMAIL)
    server.login(secrets.SENDER_EMAIL, secrets.SENDER_PASSWORD)
    for email_address in email_list:
        # Send emails in multiple part messages
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = secrets.SENDER_EMAIL
        msg['To'] = email_address
        # HTML of email content
        html = '''\
        <html>
          <head></head>
          <body>
            <p>
                <b style='font-size:20px'>Hello to my favorite person!</b>,<br><br>
                I am ecstatic to report that the following posts may be of interest to you:<br>
            </p>
            %s
            <p>
                <b style='font-size:20px'>With love from your reddit notification script <span style='color:#e06d81'>♥</span></b>
            </p>
          </body>
        </html>
        ''' 
        msg.attach(MIMEText(html, 'html'))
        server.sendmail(secrets.SENDER_EMAIL, email_address, msg.as_string())
    server.quit()
if __name__ == "__main__":
	print("hello world")
	send_email()