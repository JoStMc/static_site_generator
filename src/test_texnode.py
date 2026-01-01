import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("Image node", TextType.IMAGE, "https://cdn.britannica.com/45/125645-050-A817FE34/Common-raven.jpg")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)


    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node2 = TextNode("Image of a raven.", TextType.IMAGE, "https://cdn.britannica.com/45/125645-050-A817FE34/Common-raven.jpg")
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "img")
        self.assertEqual(html_node2.value, '')
        self.assertEqual(html_node2.tag, 'img')
        self.assertEqual(html_node2.props["src"], node2.url)
        self.assertEqual(html_node2.props["alt"], "Image of a raven.")


if __name__ == "__main__":
    unittest.main()
