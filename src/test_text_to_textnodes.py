import unittest
from inline_builder import *
from textnode import *

class TestTextToTextNodes(unittest.TestCase):
    def one_of_each(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![image](img_link) and a [link](link)")
        nodes_output = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img_link"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "link"),
                ]
        self.assertListEqual(nodes, nodes_output)

        
if __name__ == "__main__":
    unittest.main()

