import os

from chalicelib.resources import UserDB

from .common import BaseSpec


class UserDBSpec(BaseSpec):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._user_db = UserDB(cls._dynamodb, cls._table_name)

        
    def testAddUserPersistsData(self):
        email = "user@test.com"
        passcode = os.urandom(64)
        salt = os.urandom(8)

        with self.subTest("add_user does not raise exception"):
            self._user_db.add_user(email, passcode, salt)

        with self.subTest("get_user retrieves previous added user"):
            user = self._user_db.get_user(email)
            self.assertDictEqual(
                user, {
                    "email": email,
                    "passcode": passcode,
                    "salt": salt,
                    "email_verified": True})

        new_passcode = os.urandom(64)
        new_salt = os.urandom(8)
        with self.subTest("update_user_crendentials updates user passcode and salt"):
            self._user_db.update_user_crendentials(email, new_passcode, new_salt)
            user = self._user_db.get_user(email)
            self.assertDictEqual(
                user, {
                    "email": email,
                    "passcode": new_passcode,
                    "salt": new_salt,
                    "email_verified": True})
