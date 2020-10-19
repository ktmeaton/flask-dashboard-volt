from flask_mail import Message
from app import mail
from decouple import config


def send_email(to, subject, template):
    msg = Message(
        subject, recipients=[to], html=template, sender=config("MAIL_DEFAULT_SENDER"),
    )
    mail.send(msg)
