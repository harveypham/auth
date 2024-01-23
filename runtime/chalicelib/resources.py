import boto3

class UserDB:

    def __init__(self, dynamodb, table_name):
        self._user_table = dynamodb.Table(table_name)

    def add_user(self, email: str, passcode: bytes, salt: bytes):
        user = {
            "PK": self.email_to_pk(email),
            "SK": "User",
            "email": email,
            "passcode": passcode,
            "salt": salt,
            "email_verified": True # TODO: Implement email verification
        }
        self._user_table.put_item(Item=user)
    
    def get_user(self, email: str) -> str:
        user = self._user_table.get_item(Key={"PK": self.email_to_pk(email), "SK": "User"})["Item"]
        del user["PK"]
        del user["SK"]
        return user
    
    def update_user_crendentials(self, email:str, passcode: str, salt: str):
        key = {"PK": self.email_to_pk(email), "SK": "User"}
        updates = {"passcode": passcode, "salt": salt}
        self._user_table.update_item(Key=key, AttributeUpdates=updates)

    @staticmethod
    def email_to_pk(email):
        return f"USR#{email}" # TODO: use hash