import unittest
from splitter import *
from textnode import *

class TestSplitNodesImage(unittest.TestCase):

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

    def test_empty_input(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image([node])
        expected = []
        self.assertEqual(result, expected)

    def test_image_with_special_characters_in_url(self):
        node = TextNode("Image with special characters ![image](https://example.com/image?name=hello&size=large.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Image with special characters ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image?name=hello&size=large.png")
        ]
        self.assertEqual(result, expected)
        
if __name__ == "__main__":
    unittest.main()

