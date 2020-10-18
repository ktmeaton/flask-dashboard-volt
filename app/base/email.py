from flask_mail import Message
from app import mail
from decouple import config
from config import config_dict


def send_email(to, subject, template):
    print(dir(mail))
    mode = "Debug" if config("DEBUG", default=True) else "Production"
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=config_dict[mode].MAIL_DEFAULT_SENDER,
    )
    mail.send(msg)
