import os
import shutil
import sys
from generate_page import generate_page

def main():
    if not os.path.exists("docs"):
        os.mkdir("docs")

    for item in os.listdir("docs"):
        item_path = os.path.join("docs", item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    copy_static_to_docs("static", "docs")
    generate_all_pages(basepath, "content", "docs")


def copy_static_to_docs(from_path, to_path):
    items = os.listdir(from_path)
    for item in items:
        new_from_path = os.path.join(from_path, item)
        new_to_path = os.path.join(to_path, item)
        if os.path.isdir(new_from_path):
            os.mkdir(new_to_path)
            copy_static_to_docs(new_from_path, new_to_path)
        else:
            shutil.copy(new_from_path, new_to_path)


def generate_all_pages(basepath, from_path, to_path):
    items = os.listdir(from_path)
    for item in items:
        new_from_path = os.path.join(from_path, item)
        new_to_path = os.path.join(to_path, item)
        if os.path.isdir(new_from_path):
            os.mkdir(new_to_path)
            generate_all_pages(basepath, new_from_path, new_to_path)
        else:
            new_to_path = new_to_path.replace(".md", ".html")
            generate_page(basepath, new_from_path, "template.html", new_to_path)


main()
