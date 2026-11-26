import os
import unittest
from unittest.mock import patch

os.environ.pop("DB_NAME", None)
os.environ.setdefault("SECRET_KEY", "test-secret-only")

from app import app


class FakeOllama:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def raise_for_status(self):
        pass

    def iter_lines(self):
        yield b'{"message":{"content":"Moi!"}}'


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_empty_message(self):
        response = self.client.post("/chat", json={"message": ""})
        self.assertEqual(response.status_code, 400)

    @patch("app.requests.post", return_value=FakeOllama())
    def test_chat_and_history(self, mock_post):
        response = self.client.post("/chat", json={"message": "Hei"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Moi!")

        history = self.client.get("/history").json
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "Hei")
        self.assertEqual(history[1]["content"], "Moi!")


if __name__ == "__main__":
    unittest.main()
