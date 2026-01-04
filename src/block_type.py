from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown):
    if not markdown:
        return

    beginning_char = markdown[0]
    length = len(markdown)

    if re.match(r'^#{1,6} ', markdown[:min(8, length)]):
            return BlockType.HEADING

    if beginning_char == "`":
        if length > 6:
            if markdown[:3] == "```" and markdown[-3:] == "```":
                return BlockType.CODE
        return BlockType.PARAGRAPH

    lines = markdown.split("\n")

    if beginning_char == '>':
        for line in lines:
            if line[0] != '>':
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if beginning_char == '-':
        for line in lines:
            if len(line) < 2:
                return BlockType.PARAGRAPH
            if line[:2] != "- ":
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if beginning_char == '1':
        for i in range(len(lines)):
            if len(lines[i]) < 2:
                return BlockType.PARAGRAPH
            if not lines[i].startswith(str(i + 1) + '.'):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
