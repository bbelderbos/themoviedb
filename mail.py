from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import smtplib

class Mail:
  def __init__(self, sender):
    self.sender = sender

  def mail_html(self, recipients, subject, content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = self.sender
    msg['To'] = ", ".join(recipients)
    part = MIMEText(content, 'html')
    msg.attach(part)
    s = smtplib.SMTP('localhost')
    s.sendmail(self.sender, recipients, msg.as_string())
    s.quit()

if __name__ == "__main__":
  m = Mail("someemail@hotmail.com")
  m.mail_html(["bob@gmail.com"], "hi", "my message")
