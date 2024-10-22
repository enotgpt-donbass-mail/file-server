from datetime import datetime

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from src.settings import settings


class Authorization:
    def __init__(self, token: HTTPAuthorizationCredentials = None, protected: bool=False, available_roles: list[str] = None):
        self.roles = available_roles
        self.user_id = None
        self.token = token
        self.token_roles = []

        if protected:
            self.verify_jwt_token()
            self.token_has_role()


    def verify_jwt_token(self):
        token = self.token.credentials
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            self.token_roles = decoded_token['roles']
            self.user_id = decoded_token['id']
            expiration_time = decoded_token.get("exp")
            if expiration_time:
                current_time = datetime.utcnow()
                if current_time < datetime.fromtimestamp(expiration_time):
                    return decoded_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Срок действия токена истёк. Обрaтитесь за новым токеном")
        except jwt.JWTError:
            raise HTTPException(401, "Неверный токен")
        raise HTTPException(401, "Токен недействителен")


    def token_has_role(self):
        if not self.roles:
            self.roles = ['*']
        if self.roles == ['*']:
            return True
        for available_role in self.roles:
            if available_role in self.token_roles:
                return True
        raise HTTPException(401, "Access denied")

