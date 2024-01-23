from .resources import UserDB
from .crypto import PasswordHash, TokenHandler
from chalice.app import UnauthorizedError
from secrets import compare_digest


class Users:

    def __init__(self, user_db: UserDB) -> None:
        self._user_db = user_db
        # TODO: customize from config
        self._password_hash = PasswordHash() 
        self._token_handler = TokenHandler("b1b36d29-18ac-4671-a9c6-59b5ecedecca")

    def register_user(self, email: str, password: str):
        derived_key, salt = self._password_hash.derive_key(password)
        self._user_db.add_user(email, derived_key, salt)
        # TODO: catch user exists error

    def authenticate(self, email: str, password: str):
        user = self._user_db.get_user(email)
        derived_key, _ = self._password_hash(password, user["salt"])
        if not compare_digest(derived_key, user["passcode"]):
            raise UnauthorizedError()
        
        claims = {
            "sub": email,
            "aud": "app"
        }

        access_code = self._token_handler.encode(claims) # TODO: add refresh_code as well
        return {"access_code": access_code}
    
    def reset_password(self, email:str, old_password: str, new_password: str):
        user = self._user_db.get_user(email)
        derived_key, _ = self._password_hash(old_password, user["salt"])
        if not compare_digest(derived_key, user["passcode"]):
            raise UnauthorizedError()
        
        derived_key, salt = self._password_hash.derive_key(new_password)
        self._user_db.update_user_crendentials(email, derived_key, salt)


    def verify_token(self, token: str):
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        return self._token_handler.verify(token)
        

            
