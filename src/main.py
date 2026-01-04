import os
import shutil
from markdown_to_html import *

def main():
    if not os.path.exists("static"):
        raise Exception("No static files found.")

    if not os.path.exists("public"):
        os.mkdir("public")

    for item in os.listdir("public"):
        item_path = os.path.join("public", item)
        if os.path.isdir(item):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    
    copy_static_to_public("static", "public")

def copy_static_to_public(from_path, to_path):
    items = os.listdir(from_path)
    for item in items:
        new_from_path = os.path.join(from_path, item)
        new_to_path = os.path.join(to_path, item)
        if os.path.isdir(new_from_path):
            os.mkdir(new_to_path)
            copy_static_to_public(new_from_path, new_to_path)
        else:
            shutil.copy(new_from_path, new_to_path)


main()
