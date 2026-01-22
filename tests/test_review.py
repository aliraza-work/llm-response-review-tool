import unittest
from src.review import validate_pair

class ReviewTests(unittest.TestCase):
    def test_flags_missing_and_format(self):
        issues = validate_pair({"id":"1","prompt":"x","response":"plain","instruction_check":"ok","expected_format":"bullets"})
        self.assertIn("format:expected_bullets", issues)

if __name__ == "__main__":
    unittest.main()
