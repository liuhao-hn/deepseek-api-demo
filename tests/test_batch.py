import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from batch_extract import extract_lines


def _client():
    c = MagicMock()
    c.chat.completions.create.return_value.choices[0].message.content = "组件X"
    return c


class TestExtractLines(unittest.TestCase):
    def test_calls_per_line(self):
        c = _client()
        results = extract_lines(["穿模的手臂", "披风穿模"], model="m", client=c)
        self.assertEqual(len(results), 2)
        self.assertEqual(c.chat.completions.create.call_count, 2)

    def test_skips_empty_lines(self):
        c = _client()
        results = extract_lines(["", "   ", "a", "  b  "], model="m", client=c)
        self.assertEqual(len(results), 2)
        self.assertEqual(c.chat.completions.create.call_count, 2)

    def test_keeps_original_text(self):
        c = _client()
        results = extract_lines(["左手臂穿模"], model="m", client=c)
        self.assertEqual(results[0][0], "左手臂穿模")


if __name__ == "__main__":
    unittest.main()
