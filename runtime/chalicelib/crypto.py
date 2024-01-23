import os
from hashlib import pbkdf2_hmac
from datetime import datetime, timedelta


import jwt

_DT_FORMAT = "%d/%m/%Y %H:%M:%S.%f"

class PasswordHash:

    def __init__(self, iterations: int = 10000, algorithm: str = "SHA256", key_length=64):
        self._iterations = iterations
        self._algorithm = algorithm
        self._key_length = key_length

    def derive_key(self, password: str, salt: bytes = None) -> bytes:
        if salt is None:
            salt = os.urandom(8)
        hash = pbkdf2_hmac(self._algorithm, password.encode(), salt, self._iterations, self._key_length)
        return hash, salt
        
class TokenHandler:
    def __init__(self, key, algorithm: str = "HS256"):
        self._key = key
        self._algorithm = algorithm

    def encode(self, data: dict[str, str]):
        return jwt.encode(data, self._key, self._algorithm)
    
    def decode(self, token):
        return jwt.decode(token, self._key, self._algorithm)
    
    def generate(self, claims: dict[str, str], expired_in_mins): 
        now = datetime.now()
        expired_at = now + timedelta(minutes=expired_in_mins)
        claims["exp"]: self.dt_to_str(expired_at)
        claims["nbf"]: self.dt_to_str(now)
        claims["iat"]: claims["nbf"]
        return self.encode(claims)
    
    def verify(self, token: str):
        now = datetime.now()
        claims = self.decode(token)
        if self.str_to_dt(claims["nbf"]) < now < self.str_to_dt(claims["exp"]):
            raise jwt.InvalidTokenError("Token time is out of range")
        return claims

    @staticmethod
    def dt_to_str(dt: datetime):
        return dt.strftime(_DT_FORMAT)
    
    @staticmethod
    def str_to_dt(dt_str: str):
        return datetime.strptime(dt_str, _DT_FORMAT)