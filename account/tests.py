from django.test import TestCase

import json
from .models import User, Message
from .utils.message import create_message
from issue.models import *
from comment.models import Comment
import sys

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


class LoginBlackBoxTests(TestCase):
    fixtures = ["acc.json"]
    def setUp(self) -> None:
        print("Before Black Box Test")

    def tearDown(self) -> None:
        print("After Black Box Test")

    def test_register_black_box(self):
        print("Test 1: len=5, char, unique")
        x = User.objects.create(username="nomis", password="123456", email="test1@outlook.com")
        print("Registered:", x)

        print("Test 2: len=105, char, unique")
        x = User.objects.create(username="nomis"*21, password="123456", email="test2@outlook.com")
        print("Registered:", x)

        print("Test 3: len=3, number, unique")
        try:
            x = User.objects.create(username=123, password="123456", email="test3@outlook.com")
            print("Registered:", x)
        except TypeError:
            print("Found Type error!")

        print("Test 4: len=0, char, unique")
        x = User.objects.create(username="", password="123456", email="test4@outlook.com")
        print("Registered:", x)

        print("Test 5: len=100, char, unique")
        x = User.objects.create(username="nomis"*20, password="123456", email="test5@outlook.com")
        print("Registered:", x)

        print("Test 6: len=5, char, not unique")
        try:
            x = User.objects.create(username="nomis", password="123456", email="test5@outlook.com")
            print("Registered:", x)
        except:
            print(sys.exc_info())


class MessageBlackBoxTests(TestCase):
    fixtures = ["acc.json"]
    def setUp(self) -> None:
        print("Before Black Box Test")

    def tearDown(self) -> None:
        print("After Black Box Test")

    def test_create_message_black_box(self):
        print("Test 1: 0, answer")
        type = 0
        obj = Answer.objects.get(id=7)
        try:
            create_message(type, obj)
            message = Message.objects.get(Type=type, answer_id=obj.id)
            print("Create:", message)
        except:
            print(sys.exc_info())

        print("Test 2: 3, answer")
        type = 3
        obj = Answer.objects.get(id=7)
        try:
            create_message(type, obj)
            message = Message.objects.get(Type=type, answer_id=obj.id)
            print("Create:", message)
        except:
            print(sys.exc_info())

        print("Test 3: 0, None")
        type = 0
        obj = None
        try:
            create_message(type, obj)
            message = Message.objects.get(Type=type, answer_id=obj.id)
            print("Create:", message)
        except:
            print(sys.exc_info())

        print("Test 4: 0, comment")
        type = 0
        obj = Comment.objects.get(id=10)
        try:
            create_message(type, obj)
            message = Message.objects.get(Type=type, answer_id=obj.id)
            print("Create:", message)
        except:
            print(sys.exc_info())

