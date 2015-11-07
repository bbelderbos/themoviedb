#!/usr/bin/python
# -*- coding: utf-8 -*- 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import smtplib

class Mail:
  def __init__(self, sender):
    self.sender = sender

  def mail_html(self, recipients, subject, content):
    toaddr = ["info@bobbelderbos.com"]
    bcc = recipients
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = self.sender
    msg['To'] = toaddr # mask bcc, so email list receivers don't see each others emails
    part = MIMEText(content, 'html')
    msg.attach(part)
    s = smtplib.SMTP('localhost')
    s.sendmail(self.sender, toaddr + bcc, msg.as_string()) 
    s.quit()

if __name__ == "__main__":
  m = Mail("someemail@hotmail.com")
  m.mail_html(["bob@gmail.com"], "hi", "my message")
