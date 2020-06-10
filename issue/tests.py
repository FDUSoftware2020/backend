from django.test import TestCase

# Create your tests here.
import json


class IssueViewTest(TestCase):
    fixtures = ["acc.json"]

    def setUp(self) -> None:
        print("Before")

    def tearDown(self) -> None:
        print("After")

    def test_issue_create(self):
        url = "/issue/create/"
        print("Test 1: Create without login")
        response = self.client.post(url,
                                    json.dumps({"type": 0, "title": "test_title", "content": "this is a test issue"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test issue create without login:", data)
        print("=============================================")

        print("Test 2: Create issue with login")
        url_login = "/account/login/"
        response = self.client.post(url_login, json.dumps({"username": "starshine", "password": "010203"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("login_before_create_issue:", data)
        response = self.client.post(url,
                                    json.dumps({"type": 0, "title": "test_title", "content": "this is a test issue"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test issue create with login:", data)
        print("=============================================")

        print("Test 3: Create article with login")
        response = self.client.post(url,
                                    json.dumps(
                                        {"type": 1, "title": "test_article", "content": "this is a test article"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test article create with login:", data)
        print("=============================================")

    def test_issue_delete(self):
        not_author = {"username": "simon", "password": "123456"}
        author = {"username": "starshine", "password": "010203"}
        issue_id = "4"  # id
        print("Test 1: delete without login")
        response = self.client.get("/issue/" + issue_id + "/delete/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test issue delete without login:", data)
        print("=============================================")

        print("Test 2: delete with login, invalid target id")
        login_url = "/account/login/"
        response = self.client.post(login_url, json.dumps(not_author),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("login_before_delete_issue:", data)

        response = self.client.get("/issue/" + "100" + "/delete/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test issue delete with login, invalid target id:", data)
        print("=============================================")

        print("Test 3: delete with login, valid target id, not author")
        response = self.client.get("/issue/" + issue_id + "/delete/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test issue delete with login, valid target id, not author:", data)
        print("=============================================")

        # logout and login as author
        print("Test 4: delete with login, valid target id, author")
        self.client.get("/account/logout/")
        response = self.client.post(login_url, json.dumps(author),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("login_as_author_before_delete_issue:", data)
        response = self.client.get("/issue/" + issue_id + "/delete/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test issue delete with login, valid target id, author:", data)
        print("=============================================")

    def test_issue_search(self):
        url = "/issue/search/"
        print("Test 1: Failed Search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], -1)
        print("test failed search", data)
        print("=============================================")

        print("Test 2: Successful Search")
        response = self.client.post(url, json.dumps({"keyword": "红黑树"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["err_code"], 0)
        print("test successful search", data)
        print("=============================================")
