# -*- coding: utf-8 -*-

#TODO: Find more elegant solution to imports.
#       General idea is to not require modules not in use.

def notify_email(sender, to, subject, text):
    import smtplib
    try:
        from email.mime.text import MIMEText
    except ImportError:
        from email.MIMEText import MIMEText

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['to'] = to

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, [to,], msg.as_string())
    s.quit()

def notify_sms(id, sender, reciever, message):
    from tele2sms import Tele2SMS

    sms = Tele2SMS(id, sender)
    sms.send(reciever, message)