from textnode import *
from htmlnode import *

def main():
    link = { "href": "https://www.google.com",
    "target": "_blank", }
    example = HTMLNode('a', "google", props=link)
    
    print(example)


main()
