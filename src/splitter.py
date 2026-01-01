from textnode import *

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
