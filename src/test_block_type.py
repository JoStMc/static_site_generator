import unittest
from block_type import *

class TestBlockType(unittest.TestCase):
    def test_headings(self):
        single = "# A"
        self.assertEqual(block_to_block_type(single), BlockType.HEADING)

        double = "## Heading 2"
        self.assertEqual(block_to_block_type(double), BlockType.HEADING)

        no_space = "###Heading 3"
        self.assertEqual(block_to_block_type(no_space), BlockType.PARAGRAPH)

        seven = "####### Heading 7"
        self.assertEqual(block_to_block_type(seven), BlockType.PARAGRAPH)

        
    def test_code_blocks(self):
        three = "```"
        self.assertEqual(block_to_block_type(three), BlockType.PARAGRAPH)

        code = "```print('hello world')```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

        malformed =  "``print('hello world')```"
        self.assertEqual(block_to_block_type(malformed), BlockType.PARAGRAPH)

    def test_quotes(self):
        single = "> One original thought is worth a thousand mindless quotings"
        self.assertEqual(block_to_block_type(single), BlockType.QUOTE)

        several = ">This\n>is a\n>quote"
        self.assertEqual(block_to_block_type(several), BlockType.QUOTE)

        split =  ">This\n>\n>is a\n>quote"
        self.assertEqual(block_to_block_type(split), BlockType.QUOTE)

        malformed = "> This\nis a\n>quote"
        self.assertEqual(block_to_block_type(malformed), BlockType.PARAGRAPH)

    def test_unordered_lists(self):
        single = "- List"
        self.assertEqual(block_to_block_type(single), BlockType.UNORDERED_LIST)

        several = "- This\n- is a\n- list"
        self.assertEqual(block_to_block_type(several), BlockType.UNORDERED_LIST)

        malformed = "- This\n-is a\n- list"
        self.assertEqual(block_to_block_type(malformed), BlockType.PARAGRAPH)

    def test_ordered_lists(self):
        single = "1. Ordered list"
        self.assertEqual(block_to_block_type(single), BlockType.ORDERED_LIST)

        several = "1. This\n2. is a\n3. list"
        self.assertEqual(block_to_block_type(several), BlockType.ORDERED_LIST)

        no_dot =  "1. This\n2 is a\n3. list"
        self.assertEqual(block_to_block_type(no_dot), BlockType.PARAGRAPH)

        start_at_two = "2. This\n3. is a\n4. list"
        self.assertEqual(block_to_block_type(start_at_two), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()

