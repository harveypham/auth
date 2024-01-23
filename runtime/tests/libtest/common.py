import unittest

import boto3

_ENDPOINT_URL = "http://localhost:4566"


class BaseSpec(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dynamodb = boto3.resource("dynamodb", endpoint_url=_ENDPOINT_URL)
        cls._table_name = "Users"
        cls._createUserTable()

    @classmethod
    def tearDownClass(cls):
        cls.deleteUserTable()

    @classmethod
    def deleteUserTable(cls):
        try:
            table = cls._dynamodb.Table(cls._table_name)
            table.delete()
            table.wait_until_not_exists()
        except Exception as e:
            print("Failed to delete table. Please try again after a moment. Error")
            print(e)
    
    @classmethod
    def _createUserTable(cls):
        table = cls._dynamodb.create_table(
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
           ],
           ProvisionedThroughput={
               "ReadCapacityUnits": 10,
               "WriteCapacityUnits": 10
           })
        table.wait_until_exists()

if __name__ == "__main__":
    BaseSpec.setUpClass()        