import unittest

from markdown_to_html import *


class TestMDToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
                )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
                )


    def test_headings(self):
        md = """
# Heading 1

Paragraph text _italic_.

## Heading 2

###### _Heading_ 6 in italic
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><h1>Heading 1</h1><p>Paragraph text <i>italic</i>.</p><h2>Heading 2</h2><h6><i>Heading</i> 6 in italic</h6></div>"
                )

    def test_quotes(self):
        single_quote = "> This is a quote."
        node1 = markdown_to_html_node(single_quote)
        html1 = node1.to_html()
        self.assertEqual(html1, "<div><blockquote>This is a quote.</blockquote></div>")

        double_quote = """
> This is a quote.
> Second line.
"""
        node2 = markdown_to_html_node(double_quote)
        html2 = node2.to_html()
        self.assertEqual(html2, "<div><blockquote>This is a quote. Second line.</blockquote></div>")

# RECONSIDER THIS
        split_quote = """
> This is a quote.
>
> Second line.
"""
        node3 = markdown_to_html_node(split_quote)
        html3 = node3.to_html()
        self.assertEqual(html3, "<div><blockquote>This is a quote.  Second line.</blockquote></div>")

    def test_unordered_lists(self):
        single_element = "- element 1"
        node = markdown_to_html_node(single_element)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>element 1</li></ul></div>")

        two_elements = """
- element 1
- element 2
"""
        node2 = markdown_to_html_node(two_elements)
        html2 = node2.to_html()
        self.assertEqual(html2, "<div><ul><li>element 1</li><li>element 2</li></ul></div>")

        formatted_list = "- element, **but in bold**"
        node3 = markdown_to_html_node(formatted_list)
        html3 = node3.to_html()
        self.assertEqual(html3, "<div><ul><li>element, <b>but in bold</b></li></ul></div>")


    def test_ordered_lists(self):
        single_element = "1. element 1"
        node = markdown_to_html_node(single_element)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>element 1</li></ol></div>")

        two_elements = """
1. element 1
2. element 2
"""
        node2 = markdown_to_html_node(two_elements)
        html2 = node2.to_html()
        self.assertEqual(html2, "<div><ol><li>element 1</li><li>element 2</li></ol></div>")

        formatted_list = "1. element, **but in bold**"
        node3 = markdown_to_html_node(formatted_list)
        html3 = node3.to_html()
        self.assertEqual(html3, "<div><ol><li>element, <b>but in bold</b></li></ol></div>")

if __name__ == "__main__":
    unittest.main()
