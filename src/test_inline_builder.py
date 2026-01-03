import unittest

from textnode import *
from inline_builder import *


class TestInlineBuilder(unittest.TestCase):
    def test_delim_splitter(self):
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


    def test_delim_splitter_exceptions(self):
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

    def test_single_image(self):
        node = TextNode("Here is an image ![alt text](https://example.com/image.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode("Check these images ![image1](https://example.com/image1.png) and ![image2](https://example.com/image2.jpg)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Check these images ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://example.com/image1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/image2.jpg")
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Just some plain text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        node = TextNode("![image1](https://example.com/image1.png) is the first image", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("image1", TextType.IMAGE, "https://example.com/image1.png"),
            TextNode(" is the first image", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        node = TextNode("This is an image at the end ![image2](https://example.com/image2.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("This is an image at the end ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/image2.png")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images_within_text(self):
        node = TextNode("Here is ![image1](https://example.com/image1.png) and ![image2](https://example.com/image2.jpg) in text", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://example.com/image1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/image2.jpg"),
            TextNode(" in text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_invalid_image_markdown(self):
        # Edge case with malformed markdown (no closing parentheses or brackets)
        node = TextNode("This is ![image](https://example.com/image.png", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("This is ![image](https://example.com/image.png", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_image_with_special_characters_in_url(self):
        node = TextNode("Image with special characters ![image](https://example.com/image?name=hello&size=large.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Image with special characters ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image?name=hello&size=large.png")
        ]
        self.assertEqual(result, expected)

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
