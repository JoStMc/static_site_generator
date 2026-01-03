from textnode import *
from link_extractor import *


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)


    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("No matching closing delimeter found.")

        parity = 0
        if split_node[0] == '':
            parity = 1
        if split_node[-1] == '':
            split_node.pop()

        for i in range(parity, len(split_node)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            else: 
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes


def _split_nodes_generic(old_nodes, extract_fn, build_md, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_fn(node.text)

        split_text = [node.text]
        for link in links:
            # Link must always appear in ultimate split as they are extracted in order
            # Take all but last split + the last with only the first occurrence split
            split_text = split_text[:-1] + split_text[-1].split(build_md(link[0], link[1]), 1)

        for i in range(len(split_text)):
            if i > 0:
                new_nodes.append(TextNode(links[i-1][0], text_type, links[i-1][1]))
            if not split_text[i]:
                continue
            new_nodes.append(TextNode(split_text[i], TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_generic(
            old_nodes,
            extract_markdown_images,
            lambda alt, url: f"![{alt}]({url})",
            TextType.IMAGE,
            )

def split_nodes_link(old_nodes):
    return _split_nodes_generic(
            old_nodes,
            extract_markdown_links,
            lambda text, url: f"[{text}]({url})",
            TextType.LINK,
            )
