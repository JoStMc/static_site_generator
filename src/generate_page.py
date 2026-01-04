import re
from markdown_to_html import markdown_to_html_node
from htmlnode import *

def extract_title(markdown):
    header = re.findall(r"^# (.*$)", markdown, re.MULTILINE)
    if not header:
        raise Exception("No header found")
    return header[0]


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path, 'r') as md_f:
        markdown = md_f.read()
    with open(template_path, 'r') as tp_f:
        template = tp_f.read()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = (template.replace("{{ Title }}", title).
            replace("{{ Content }}", content))
    
    with open(dest_path, 'w') as dest_f:
        dest_f.write(html)
