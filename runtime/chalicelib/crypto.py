import os
from hashlib import pbkdf2_hmac
from datetime import datetime, timedelta, timezone


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
        now = self.utc_now()
        expired_at = now + timedelta(minutes=expired_in_mins)
        claims["exp"] = expired_at
        claims["nbf"] = now
        claims["iat"] = claims["nbf"]
        return self.encode(claims)
    
    def verify(self, token: str):
        claims = self.decode(token)
        return claims

    @staticmethod
    def dt_to_str(dt: datetime):
        return dt.strftime(_DT_FORMAT)
    
    @staticmethod
    def str_to_dt(dt_str: str):
        return datetime.strptime(dt_str, _DT_FORMAT)
    
    @staticmethod
    def utc_now():
        return datetime.now(tz=timezone.utc)