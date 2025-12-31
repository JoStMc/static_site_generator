import unittest

from htmlnode import *


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
        self.assertEqual(no_link.props_to_html(), "")


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
        node1 = LeafNode("a", "google", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), "<a href=\"https://www.google.com\">google</a>")

        node2 = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node2.to_html()

        node3 = LeafNode(None, "raw text")
        self.assertEqual(node3.to_html(), "raw text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        bold_child = LeafNode('b', "bold text")
        normal_child = LeafNode(None, "normal text")
        italic_child = LeafNode('i', "italic text")
        parent_p = ParentNode('p', [bold_child, normal_child, italic_child, normal_child])
        self.assertEqual(parent_p.to_html(), "<p><b>bold text</b>normal text<i>italic text</i>normal text</p>")

        childless = ParentNode("div", None)
        tagless = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            childless.to_html()
            tagless.to_html()
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        bottom_link = LeafNode('a', "click here", {"href": "https://google.com"})
        bottom_text = LeafNode(None, "in bold")
        middle_bold = ParentNode('b', [bottom_text, bottom_link])
        middle_text = LeafNode(None, "Example of a link")
        top = ParentNode('p', [middle_text, middle_bold])

        self.assertEqual(top.to_html(), "<p>Example of a link<b>in bold<a href=\"https://google.com\">click here</a></b></p>")

if __name__ == "__main__":
    unittest.main()
