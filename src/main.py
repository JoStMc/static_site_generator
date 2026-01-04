import os
import shutil
from generate_page import generate_page

def main():
    if not os.path.exists("public"):
        os.mkdir("public")

    for item in os.listdir("public"):
        item_path = os.path.join("public", item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    
    copy_static_to_public("static", "public")
    generate_all_pages("content", "public")


def generate_page_wrapped(from_path, to_path):
    to_path = to_path.replace(".md", ".html")
    return generate_page(from_path, "template.html", to_path)

def copy_static_to_public(from_path, to_path):
    copy_files_recursive(from_path, to_path, shutil.copy)

def generate_all_pages(from_path, to_path):
    copy_files_recursive(from_path, to_path, generate_page_wrapped)

def copy_files_recursive(from_path, to_path, func):
    items = os.listdir(from_path)
    for item in items:
        new_from_path = os.path.join(from_path, item)
        new_to_path = os.path.join(to_path, item)
        if os.path.isdir(new_from_path):
            os.mkdir(new_to_path)
            copy_files_recursive(new_from_path, new_to_path, func)
        else:
            func(new_from_path, new_to_path)



main()
