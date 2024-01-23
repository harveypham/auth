import os
import json

from chalice.test import Client, HTTPResponse

import _context

from libtest.common import BaseSpec, _ENDPOINT_URL


class AppSpec(BaseSpec):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._client = cls._get_app()

    @classmethod
    def _get_app(cls):
        os.environ["ENDPOINT"] = _ENDPOINT_URL
        os.environ["USER_TABLE_NAME"] = cls._table_name
        from app import app
        return Client(app)
    
    def testSpec(self):
        email = "user@test.com"
        password = "P@ssw0rd"
        headers = {"Content-Type": "application/json"}
        with self.subTest("POST /register register users"):
            response = self._client.http.post(
                "/register",
                headers=headers,
                body=json.dumps({"email": email, "password": password}))
            self.assertEqual(response.status_code, 200)

        with self.subTest("POST /login returns access token"):
            response = self._client.http.post(
                "/login",
                headers=headers,
                body=json.dumps({"email": email, "password": password}))
            self.assertEqual(response.status_code, 200)
            self.assertTrue("access_token" in response.json_body)
            headers["Authorization"] = response.json_body["access_token"]

        with self.subTest("Token can be used"):
            response = self._client.http.get("/verify", headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertTrue("sub" in response.json_body)

        with self.subTest("PUT /password changes password to new value"):
            new_password = "Test1234!"
            response = self._client.http.put(
                "/password", headers=headers,
                body=json.dumps({"password": password, "new_password": new_password}))
            self.assertEqual(response.status_code, 200)

            with self.subTest("POST /login with new password returns access token"):
                response = self._client.http.post(
                    "/login",
                    headers=headers,
                    body=json.dumps({"email": email, "password": new_password}))
                self.assertEqual(response.status_code, 200)
                self.assertTrue("access_token" in response.json_body)
                headers["Authorization"] = response.json_body["access_token"]

            with self.subTest("Token can be used"):
                response = self._client.http.get("/verify", headers=headers)
                self.assertEqual(response.status_code, 200)
                self.assertTrue("sub" in response.json_body)
