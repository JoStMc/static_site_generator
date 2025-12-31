import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_props(self):
        link = { "href": "https://www.google.com",
                "target": "_blank", }
        link_same_tab = {"href": "https://www.google.com"}
        example_link = HTMLNode('a', "google", props=link)
        example_link2 = HTMLNode('a', props=link_same_tab)
        no_link = HTMLNode('p', "sample paragraph")


        self.assertEqual(example_link.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        self.assertEqual(example_link2.props_to_html(), " href=\"https://www.google.com\"")
        self.assertEqual(no_link.props_to_html(), None)


if __name__ == "__main__":
    unittest.main()
