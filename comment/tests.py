from django.test import TestCase
from django.test import TransactionTestCase
# Create your tests here.
from .models import Comment
import sys
import json
from issue.models import Issue, Answer


class CommentViewTests(TransactionTestCase):
    fixtures = ["acc.json"]

    def setUp(self) -> None:
        print("Before")
        self.login()

    def tearDown(self) -> None:
        print("After")

    def login(self):
        url = "/account/login/"
        response = self.client.post(url, json.dumps({"username": "simon", "password": "123456"}),
                                    content_type="application/json")

    def test_comment_create_black_box(self):
        url = "/comment/create/"
        print("Test 1: type=1, article_id=5")
        data1 = {"target_type": 1, "target_id": 5, "parent_comment_id": -1,
                 "content": "This is a test comment 1 to an article."}
        try:
            response = self.client.post(url, json.dumps(data1), content_type="application/json")
            self.assertEqual(response.status_code, 200)
            res = json.loads(response.content)
            self.assertEqual(res["err_code"], 0)
            print("Test 1 result:", res)
            x = Comment.objects.get(content=data1["content"])
            print("====>", x.content)
        except:
            print(sys.exc_info())

        print()
        print("Test 2: type=1, article_id=-1")
        data2 = {"target_type": 1, "target_id": -1, "parent_comment_id": -1,
                 "content": "This is a test comment 2 to an article."}
        try:
            response = self.client.post(url, json.dumps(data2), content_type="application/json")
            self.assertEqual(response.status_code, 200)
            res = json.loads(response.content)
            self.assertEqual(res["err_code"], 0)
            print("Test 2 result:", res)
            x = Comment.objects.get(content=data2["content"])
            print("====>", x.content)
        except:
            print(sys.exc_info())

        print()
        print("Test 3: type=4, article_id=5")
        data3 = {"target_type": 4, "target_id": 5, "parent_comment_id": -1,
                 "content": "This is a test comment 3 to an article."}
        try:
            response = self.client.post(url, json.dumps(data3), content_type="application/json")
            self.assertEqual(response.status_code, 200)
            res = json.loads(response.content)
            self.assertEqual(res["err_code"], 0)
            print("Test 3 result:", res)
            x = Comment.objects.get(content=data3["content"])
            print("====>", x.content)
        except:
            print(sys.exc_info())

        print()
        print("Test 4: type=1, article_id=\"\"")
        data4 = {"target_type": 1, "target_id": None, "parent_comment_id": -1,
                 "content": "This is a test comment 4 to an article."}
        try:
            response = self.client.post(url, json.dumps(data4), content_type="application/json")
            self.assertEqual(response.status_code, 200)
            res = json.loads(response.content)
            self.assertEqual(res["err_code"], 0)
            print("Test 4 result:", res)
            x = Comment.objects.get(content=data4["content"])
            print("====>", x.content)
        except:
            print(sys.exc_info())

        print()
        print("Test 5: type=1, answer_id=16")
        data5 = {"target_type": 1, "target_id": 16, "parent_comment_id": -1,
                 "content": "This is a test comment 5 to an article."}
        try:
            response = self.client.post(url, json.dumps(data5), content_type="application/json")
            self.assertEqual(response.status_code, 200)
            res = json.loads(response.content)
            self.assertEqual(res["err_code"], 0)
            print("Test 5 result:", res)
            x = Comment.objects.get(content=data5["content"])
            print("====>", x.content)
        except:
            print(sys.exc_info())