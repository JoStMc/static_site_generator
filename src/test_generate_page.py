import unittest

from generate_page import *


class TestGeneratePage(unittest.TestCase):

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("text\n# Title"), "Title")
        self.assertEqual(extract_title("# Title\ntext"), "Title")
        self.assertEqual(extract_title("text\n# Title\ntext"), "Title")

        with self.assertRaises(Exception):
            extract_title("text\n not-starter # heading.")
            extract_title("no\nheading")


if __name__ == "__main__":
    unittest.main()
