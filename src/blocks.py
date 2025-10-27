from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.splitlines()
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith("#"):
        return BlockType.HEADING
    elif all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.strip().startswith("-") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\.", line.strip()) for line in lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    lines = markdown.strip().replace('\r\n', '\n').replace('\r', '\n').split('\n')
    blocks = []
    current_block = []
    in_code_block = False

    for line in lines:
        if line.lstrip().startswith("```"):
            if in_code_block:
                current_block.append(line)
                blocks.append("\n".join(current_block))
                current_block = []
                in_code_block = False
            else:
                if current_block:
                    blocks.append("\n".join(current_block))
                current_block = [line]
                in_code_block = True
        elif line.strip() == "" and not in_code_block:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    html_children = []
    blocks = markdown_to_blocks(markdown)
    print("Blocks:")
    for b in blocks:
        block_type = block_to_block_type(b)
        print("DETECTED TYPE ►", block_type)
        #HEADING
        if block_type == BlockType.HEADING:
            hashtag = 0
            for char in b.splitlines()[0]:
                if char == "#":
                    hashtag += 1
                else:
                    break
            text = b[hashtag + 1:].strip()
            html_children.append(HTMLNode(f"h{hashtag}", children=text_to_children(text)))
        #PARAGRAPH          
        elif block_type == BlockType.PARAGRAPH:
            lines = b.splitlines()
            text = " ".join(line.strip() for line in lines)
            html_children.append(HTMLNode(tag="p", children=text_to_children(text)))
        #QUOTE
        elif block_type == BlockType.QUOTE:
            lines = b.splitlines()
            clean_lines = []
            for line in lines:
                clean_lines.append(line.strip("> "))
            text = "\n".join(clean_lines)
            html_children.append(HTMLNode(tag="blockquote", children=text_to_children(text)))
        #UNORDERED LIST
        elif block_type == BlockType.UNORDERED_LIST:
            lines = b.splitlines()
            clean_lines = []
            for line in lines:
                clean_lines.append(line.strip("- "))
            li = []
            for clean in clean_lines:
                li.append(HTMLNode(tag="li", children=text_to_children(clean)))
            html_children.append(HTMLNode(tag="ul", children=li))
        #ORDERED LIST
        elif block_type == BlockType.ORDERED_LIST:
            lines = b.splitlines()
            clean_lines = []
            for line in lines:
                first = line.split(".", 1)[0]
                clean_lines.append(line[len(first) + 1:].strip())
            li = []
            for clean in clean_lines:
                li.append(HTMLNode(tag="li", children=text_to_children(clean)))
            html_children.append(HTMLNode(tag="ol", children=li))
        #CODE
        elif block_type == BlockType.CODE:
            lines = b.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines) + "\n"
            code_node_html = HTMLNode(tag="pre", children=[LeafNode(tag="code", value=text)])
            html_children.append(code_node_html)
    return HTMLNode(tag="div", children=html_children)

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            print("title found")
            return line
    raise Exception("title not found")
        
    

