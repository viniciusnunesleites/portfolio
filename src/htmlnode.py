

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #string html name
        self.value = value #string html value
        self.children = children #list of htmlnode objects
        self.props = props #dictionary attributes

    def to_html(self):
        if self.tag is None:
            return str(self.value)
        props_str = self.props_to_html()
        if props_str:
            html = f"<{self.tag} {props_str}>"
        else:
            html = f"<{self.tag}>"
        if self.children:
            for child in self.children:
                html += child.to_html()
        elif self.value is not None:
            html += str(self.value)
        html += f"</{self.tag}>"
        return html

    def props_to_html(self):
        if not self.props:
            return None
        if not isinstance(self.props, dict):
            return None
        result = ""
        for keys, values in self.props.items():
           result += f'{keys}="{values}" '
        return result.rstrip()
    
    def __repr__(self):
        return f"{self.tag},{self.value},{self.children},{self.props}"
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value")
        if self.tag == None:
            return str(self.value)
        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires a tag")
        if not self.children:
            raise ValueError("ParentNode requires children")
        props_str = self.props_to_html()
        if props_str:
            opening_tag = f"<{self.tag} {props_str}>"
        else:
            opening_tag = f"<{self.tag}>"
        result = ""
        for c in self.children:
            result += c.to_html()
        return f"{opening_tag}{result}</{self.tag}>"