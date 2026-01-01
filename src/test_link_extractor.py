import unittest

from link_extractor import *


class TestSplitter(unittest.TestCase):
    def test_extract_markdown_images(self):
        no_image = extract_markdown_images("no image")
        self.assertListEqual([], no_image)

        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        two_images = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], two_images)


        image_and_link = extract_markdown_images("image, ![empty](sample_link), link [empty2](sample_link2)")
        self.assertListEqual([("empty", "sample_link")], image_and_link)


    def text_extract_markdown_links(self):
        no_link = extract_markdown_links("no links")
        self.assertListEqual([], no_link)

        image_and_link = extract_markdown_link("image, ![empty](sample_link), link [empty2](sample_link2)")
        self.assertListEqual([("empty2", "sample_link2")], image_and_link)

        two_links = extract_markdown_links("This is text with a link [to google](https://www.google.com) and [to youtube](https://www.youtube.com/)")
        self.assertListEqual([("to google", "https://www.google.com"), ("to youtube", "https://www.youtube.com/")], two_links)

if __name__ == "__main__":
    unittest.main()
