import unittest

import _context

from chalicelib.handlers import Users, UnauthorizedError

from .common import BaseSpec

class UsersSpec(BaseSpec):

    @classmethod
    def setUpClass(cls):
        from chalicelib.resources import UserDB
        super().setUpClass()
        user_db = UserDB(cls._dynamodb, cls._table_name)
        cls._handler = Users(user_db)

    def testUserHandler(self):
        email = "user@test.com"
        password = "P@ssw0rd"

        with self.subTest("register_user does not throw"):
            self._handler.register_user(email, password)

        with self.subTest("authenticate with wrong password raises UnauthorizedError"):
            with self.assertRaises(UnauthorizedError):
                self._handler.authenticate(email, "wrong password !!!")

        with self.subTest("authenticate with correct password returns access code"):
            auth_resp = self._handler.authenticate(email, password)
            self.assertTrue("access_token" in auth_resp)
            claims = self._handler.verify_token(auth_resp["access_token"])
            self.assertEqual(claims["sub"], email)

        with self.subTest("reset_password updates password"):
            new_password = "New password"
            self._handler.change_password(email, password, new_password)
            auth_resp = self._handler.authenticate(email, new_password)
            self.assertTrue("access_token" in auth_resp)
            claims = self._handler.verify_token(auth_resp["access_token"])
            self.assertEqual(claims["sub"], email)






