import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import apitest


def _mock_answer(content):
    client = MagicMock()
    client.chat.completions.create.return_value.choices[0].message.content = content
    return client


class TestExtract(unittest.TestCase):
    def test_returns_model_content(self):
        client = _mock_answer("左手臂, 红色披风")
        result = apitest.extract_components("穿模现象", client=client)
        self.assertEqual(result, "左手臂, 红色披风")

    def test_passes_model_and_text(self):
        client = _mock_answer("x")
        apitest.extract_components("穿模的手臂", model="deepseek-v4-flash", client=client)
        _, kwargs = client.chat.completions.create.call_args
        self.assertEqual(kwargs["model"], "deepseek-v4-flash")
        self.assertIn("穿模的手臂", kwargs["messages"][1]["content"])


class TestBuildClient(unittest.TestCase):
    def test_missing_key_exits(self):
        old = os.environ.pop("DEEPSEEK_API_KEY", None)
        try:
            with self.assertRaises(SystemExit):
                apitest.build_client()
        finally:
            if old is not None:
                os.environ["DEEPSEEK_API_KEY"] = old

    def test_with_key_builds_client(self):
        client = apitest.build_client(api_key="sk-test")
        self.assertIsNotNone(client)


if __name__ == "__main__":
    unittest.main()
