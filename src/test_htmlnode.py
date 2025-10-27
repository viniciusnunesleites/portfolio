import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode
from main import *

class TestHTMLNode(unittest.TestCase):
    def test_html_prop(self):
        node = HTMLNode("h1", "testing value paragraph", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')
    def test_html_no_prop(self):
        node = HTMLNode("h1", "testing value paragraph", None, None)
        self.assertEqual(node.props_to_html(), None)
    def test_html_not_prop(self):            
        node = HTMLNode("h1", "testing value paragraph", None, "this is not a dict so it should give me an error")
        self.assertEqual(node.props_to_html(), None)


    #test leaf
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        #test parent
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",)
    
if __name__ == "__main__":
    unittest.main()