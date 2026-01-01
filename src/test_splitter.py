import unittest

from textnode import *
from splitter import *


class TestSplitter(unittest.TestCase):
    def test_spliter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node_output = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                ]
        self.assertEqual(new_nodes, node_output)

        bold1 = TextNode("**bold** in a text.", TextType.TEXT)
        bold2 = TextNode("This is text with **bold**", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([bold1, bold2], "**", TextType.BOLD)
        bolds_output = [
                TextNode("bold", TextType.BOLD),
                TextNode(" in a text.", TextType.TEXT),
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD)
                ] 
        self.assertEqual(new_nodes2, bolds_output)

        empty_italic = TextNode("** no italic.", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([empty_italic], '*', TextType.ITALIC)
        empty_italic_output = [
                TextNode('', TextType.ITALIC),
                TextNode(" no italic.", TextType.TEXT)
                ]
        self.assertEqual(new_nodes3, empty_italic_output)

        not_text = TextNode("bold **text", TextType.BOLD)
        not_text_node = split_nodes_delimiter([not_text], "**", TextType.BOLD)
        self.assertEqual(not_text_node, [TextNode("bold **text", TextType.BOLD)])

        non_text_with_bold = split_nodes_delimiter([bold2, not_text], "**", TextType.BOLD)
        non_text_with_bold_output = [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("bold **text", TextType.BOLD),
                ]
        self.assertEqual(non_text_with_bold, non_text_with_bold_output)


    def test_exceptions(self):
        error1 = TextNode("code block` in a text", TextType.TEXT)
        error2 = TextNode("`code block in a text", TextType.TEXT)
        error3 = TextNode("code block in a text`", TextType.TEXT)
        error4 = TextNode("`code block` in a `text", TextType.TEXT)
        error5 = TextNode("code `block` in a `text", TextType.TEXT)
        error6 = TextNode("code `block` in a text`", TextType.TEXT)
        error7 = TextNode("`code block` in a text`", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([error1], "`", TextType.CODE)
            split_nodes_delimiter([error2], "`", TextType.CODE)
            split_nodes_delimiter([error3], "`", TextType.CODE)
            split_nodes_delimiter([error4], "`", TextType.CODE)
            split_nodes_delimiter([error5], "`", TextType.CODE)
            split_nodes_delimiter([error6], "`", TextType.CODE)
            split_nodes_delimiter([error7], "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()
