class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by child classes")

    def props_to_html(self):
        if self.props is None:
            return ""
        html_attrs = ""
        for key,value in self.props.items():
            html_attrs += f' {key}="{value}"'

        return html_attrs

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__( self, tag, value, props=None):
        super().__init__(tag,value,None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")

        if self.tag is None:
            return self.value

        props_html = self.props_to_html()

        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__( self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")

        if self.children is None:
            raise ValueError("Invalid HTML: no children")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

