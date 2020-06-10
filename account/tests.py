from django.test import TestCase

import json


class LoginViewTests(TestCase):
    fixtures = ["acc.json"]

    def setUp(self) -> None:
        print("Before test")

    def tearDown(self) -> None:
        print("After test")

    def test_login(self):
        url = "/account/login/"
        response = self.client.post(url, json.dumps({"username": "simon", "password": "123"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test_wrong_password_login:", data)
        response = self.client.post(url, json.dumps({"username": "starshine", "password": "010203"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test_right_password_login:", data)

    def test_verify(self):
        url = "/account/verify/"
        response = self.client.post(url, json.dumps({"email": "xrnie@outlook.com"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test_verify_right:", data)
        response = self.client.post(url, json.dumps({"email": "xrnie@outlook.com"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test_verify_wrong:", data)

    def test_register(self):
        url = "/account/register/"
        response = self.client.post(url, json.dumps({"username":"simon", "password":"123456", "verification":"0568", "email":"xrnie@outlook.com"}),content_type="application/json" )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test_register_right", data)
        response = self.client.post(url, json.dumps(
            {"username": "simon", "password": "123456", "verification": "0568", "email": "xrnie@outlook.com"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test_register_wrong", data)
    def test_logout(self):
        url = "/account/logout/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test_fail_logout:", data)
        url_login = "/account/login/"
        response = self.client.post(url_login, json.dumps({"username": "starshine", "password": "010203"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test_login_before_logout:", data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test_succeed_logout:", data)
