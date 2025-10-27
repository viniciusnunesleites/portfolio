from enum import Enum
from htmlnode import LeafNode
import re




class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE  = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text= text             #text content of the node
        self.text_type = text_type  #type of text member of textype enum
        self.url = url              #url link or image

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type  == TextType.CODE:
        return LeafNode("code", text_node.text)        
    if text_node.text_type  == TextType.LINK:
        return LeafNode("a", text_node.text, {"href" : text_node.url})
    if text_node.text_type  == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
            raise Exception("not a valid text type enum")

#split delimiters
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
    
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("thats invalid Markdown syntax")
        
        index = 0
        for part in parts:
            if index % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
            index += 1
    return new_nodes
    
    #extract markdown
def extract_markdown_images(text):
    result1 = re.findall(r"!\[(.*?)\]+\((.*?)\)", text )
    return result1

def extract_markdown_links(text):
    result2 = re.findall(r"(?<!!)\[(.*?)\]+\((.*?)\)", text )
    return result2

#split images and links
def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        match = extract_markdown_images(node.text)
        if not match:
            new_nodes.append(node)
            continue
        
        for m in match:
            alt, url = m
            image = f"![{alt}]({url})"
            sections = text.split(image, 1)
            before = sections[0]
            after = sections[1]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
                
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        match = extract_markdown_links(node.text)
        if not match:
            new_nodes.append(node)
            continue
        
        for m in match:
            alt, url = m
            label = f"[{alt}]({url})"
            sections = text.split(label, 1)
            before = sections[0]
            after = sections[1]

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(label, TextType.LINK, url))
            text = after
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
                
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    if text:
        nodes = split_nodes_images(nodes)
        nodes = split_nodes_links(nodes)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "__", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
            