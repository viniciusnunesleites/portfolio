import unittest

from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_images, split_nodes_links
from htmlnode import HTMLNode, LeafNode
from main import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq_url(self):
        node = TextNode("link test", TextType.LINK, "www.divenci.com.br")
        node2 = TextNode("link test", TextType.LINK)
        self.assertNotEqual(node, node2)
    def test_eq_text_type(self):
        node = TextNode("test text", TextType.BOLD)
        node2 = TextNode("test text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

         
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
    def test_text_to_textnodes(self):
        text = "this is a **bold** test text to textnodes function test"
        new_nodes = text_to_textnodes(text)
        expected = [
        TextNode("this is a ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" test text to textnodes function test", TextType.TEXT),
    ]
        self.assertEqual(new_nodes, expected)
    def test_text_to_textnodes_image(self):
        text = "this is test to ![gandalf](https://blabla.com/blablabla.jpeg) textnodes function test"
        new_nodes = text_to_textnodes(text)
        expected = [
        TextNode("this is test to ", TextType.TEXT),
        TextNode("gandalf", TextType.IMAGE, "https://blabla.com/blablabla.jpeg"),
        TextNode(" textnodes function test", TextType.TEXT),
    ]
        self.assertEqual(new_nodes, expected)
        
    def test_markdown_to_blocks(self):
        md = """
This is *bolded* paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is *bolded* paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
if __name__ == "__main__":
    unittest.main()