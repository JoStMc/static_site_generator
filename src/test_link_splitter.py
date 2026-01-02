import unittest
from splitter import *
from textnode import *

class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        node = TextNode("This is a link [to google](https://www.google.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "https://www.google.com")
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode("Visit [Google](https://www.google.com) and [YouTube](https://www.youtube.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com")
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Just some plain text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        node = TextNode("[Google](https://www.google.com) is a search engine", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" is a search engine", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode("This is a link to [Google](https://www.google.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is a link to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com")
        ]
        self.assertEqual(result, expected)

    def test_multiple_links_within_text(self):
        node = TextNode("Check [Google](https://www.google.com) and [YouTube](https://www.youtube.com) for videos", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com"),
            TextNode(" for videos", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_invalid_markdown(self):
        # Edge case with malformed markdown (no closing parentheses or brackets)
        node = TextNode("This is [Google(https://www.google.com", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is [Google(https://www.google.com", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_empty_input(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link([node])
        expected = []
        self.assertEqual(result, expected)
        
if __name__ == "__main__":
    unittest.main()
