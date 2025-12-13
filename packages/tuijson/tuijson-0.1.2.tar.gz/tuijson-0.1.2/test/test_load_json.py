import unittest
import json
from tjson import load_json_input


class TestLoadJson(unittest.TestCase):
    def test_load_from_string(self):
        STRING = '{"api": {"host": "localhost", "port": 8080}, "debug": true, "roles": ["admin", "user"]}'
        data, _ = load_json_input(STRING)
        self.assertEqual(data, json.loads(STRING))

    def test_load_from_file(self):
        FILE = "test/example.json"
        data, _ = load_json_input(FILE)
        with open(FILE, "r", encoding="utf-8") as f:
            self.assertEqual(data, json.load(f))

    def test_load_from_file2(self):
        FILE = "test/large_example.json"
        data, _ = load_json_input(FILE)
        with open(FILE, "r", encoding="utf-8") as f:
            self.assertEqual(data, json.load(f))


if __name__ == "__main__":
    unittest.main()
