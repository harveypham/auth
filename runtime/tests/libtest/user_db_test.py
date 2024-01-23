import unittest
import os

import boto3

import _context

from chalicelib.resources import UserDB


class UserDBSpec(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dynamodb = boto3.resource("dynamodb", endpoint_url="https://localhost:8000")
        cls._table_name = "Users"
        cls._createUserTable()
        cls._user_db = UserDB(cls._dynamodb, cls._table_name)
    
    @classmethod
    def _createUserTable(cls):
        cls._dynamodb.create_table(
            TableName=cls._table_name,
            AttributeDefinitions=[
                {
                    "AttributeName": "PK",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "SK",
                    "AttributeType": "S"
                }
           ],
           KeySchema=[
                {
                    "AttributeName": "PK",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "SK",
                    "KeyType": "RANGE"
                }
           ])
        
    def testAddUserPersistsData(self):
        email = "user@test.com"
        passcode = os.urandom(64)
        salt = os.urandom(8)

        with self.subTest("add_user does not raise exception"):
            self._user_db.add_user(email, passcode, salt)

        with self.subTest("get_user retrieves previous added user"):
            user = self._user_db.get_user(email)
            self.assertDictEqual(user, {"email": email, "passcode": passcode, "salt": salt, "email_verified": True})

        new_passcode = os.urandom(64)
        new_salt = os.urandom(8)
        with self.subTest("update_user_crendentials updates user passcode and salt"):
            self._user_db.update_user_crendentials(email, )