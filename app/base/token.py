# project/token.py

from itsdangerous import URLSafeTimedSerializer
from config import config_dict
from decouple import config


def generate_confirmation_token(email):
    mode = "Debug" if config("DEBUG", default=True) else "Production"
    serializer = URLSafeTimedSerializer(config_dict[mode].SECRET_KEY)
    return serializer.dumps(email, salt=config_dict[mode].SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    mode = "Debug" if config("DEBUG", default=True) else "Production"
    serializer = URLSafeTimedSerializer(config_dict[mode].SECRET_KEY)
    try:
        email = serializer.loads(
            token, salt=config_dict[mode].SECURITY_PASSWORD_SALT, max_age=expiration
        )
    except Exception:
        return False
    return email
