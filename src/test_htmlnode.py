import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_with_multiple_attributes(self):
        """Test props_to_html with multiple attributes"""
        node = HTMLNode("a", "Click me", None, {
            "href": "https://www.google.com",
            "target": "_blank"
        })
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html_with_single_attribute(self):
        """Test props_to_html with single attribute"""
        node = HTMLNode("p", "Paragraph", None, {"class": "highlight"})
        expected = ' class="highlight"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html_with_no_props(self):
        """Test props_to_html when props is None"""
        node = HTMLNode("p", "Paragraph")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html_with_empty_props(self):
        """Test props_to_html with empty dictionary"""
        node = HTMLNode("p", "Paragraph", None, {})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)
    
    def test_repr_method(self):
        """Test the __repr__ method"""
        node = HTMLNode("a", "Link text", None, {"href": "https://example.com"})
        expected = "HTMLNode(a, Link text, children: None, {'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)
    
    def test_to_html_raises_not_implemented_error(self):
        """Test that to_html raises NotImplementedError"""
        node = HTMLNode("p", "Test")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_constructor_defaults(self):
        """Test that constructor defaults work properly"""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_constructor_with_children(self):
        """Test constructor with children list"""
        child1 = HTMLNode("span", "Hello")
        child2 = HTMLNode("span", "World")
        parent = HTMLNode("div", None, [child1, child2])
        
        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "Hello")
        self.assertEqual(parent.children[1].value, "World")


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        """Test basic paragraph leaf node"""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        """Test anchor tag with href attribute"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        """Test leaf node with no tag (raw text)"""
        node = LeafNode(None, "Just some raw text")
        self.assertEqual(node.to_html(), "Just some raw text")

    def test_leaf_to_html_bold(self):
        """Test bold tag"""
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_italic(self):
        """Test italic tag"""
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_leaf_to_html_code(self):
        """Test code tag"""
        node = LeafNode("code", "print('hello')")
        self.assertEqual(node.to_html(), "<code>print('hello')</code>")

    def test_leaf_to_html_img_with_multiple_props(self):
        """Test img tag with multiple attributes"""
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "Test image", "width": "100"})
        expected = '<img src="image.jpg" alt="Test image" width="100"></img>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_span_with_class(self):
        """Test span tag with class attribute"""
        node = LeafNode("span", "Highlighted text", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Highlighted text</span>')

    def test_leaf_to_html_h1(self):
        """Test heading tag"""
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")

    def test_leaf_to_html_no_value_raises_error(self):
        """Test that leaf node with no value raises ValueError"""
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no value")

    def test_leaf_to_html_empty_string_value(self):
        """Test leaf node with empty string value (should work)"""
        node = LeafNode("br", "")
        self.assertEqual(node.to_html(), "<br></br>")

    def test_constructor_no_children(self):
        """Test that LeafNode constructor sets children to None"""
        node = LeafNode("p", "Test")
        self.assertIsNone(node.children)

    def test_constructor_with_props(self):
        """Test constructor with props"""
        props = {"href": "https://example.com", "target": "_blank"}
        node = LeafNode("a", "Link", props)
        self.assertEqual(node.props, props)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link")

    def test_constructor_without_props(self):
        """Test constructor without props"""
        node = LeafNode("p", "Paragraph")
        self.assertIsNone(node.props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Paragraph")

class TestParentNode(unittest.TestCase):
    
    def test_to_html_with_children(self):
        """Test basic parent node with single child"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        """Test nested parent nodes (grandchildren)"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_multiple_children(self):
        """Test parent node with multiple leaf children"""
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode(None, "Normal text")
        
        parent = ParentNode("p", [child1, child2, child3, child4])
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_with_props(self):
        """Test parent node with HTML attributes"""
        child = LeafNode("span", "Click here")
        parent = ParentNode("a", [child], {"href": "https://example.com", "target": "_blank"})
        expected = '<a href="https://example.com" target="_blank"><span>Click here</span></a>'
        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_deeply_nested(self):
        """Test deeply nested parent nodes"""
        deep_child = LeafNode("strong", "Deep text")
        level3 = ParentNode("em", [deep_child])
        level2 = ParentNode("span", [level3])
        level1 = ParentNode("p", [level2])
        root = ParentNode("div", [level1])
        
        expected = "<div><p><span><em><strong>Deep text</strong></em></span></p></div>"
        self.assertEqual(root.to_html(), expected)
    
    def test_to_html_mixed_children_types(self):
        """Test parent with both leaf and parent children"""
        leaf1 = LeafNode(None, "Start ")
        nested_parent = ParentNode("b", [LeafNode("i", "bold italic")])
        leaf2 = LeafNode(None, " end.")
        
        parent = ParentNode("p", [leaf1, nested_parent, leaf2])
        expected = "<p>Start <b><i>bold italic</i></b> end.</p>"
        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_single_leaf_child(self):
        """Test parent with single leaf child"""
        child = LeafNode("h1", "Title")
        parent = ParentNode("header", [child])
        self.assertEqual(parent.to_html(), "<header><h1>Title</h1></header>")
    
    def test_to_html_multiple_parent_children(self):
        """Test parent with multiple parent children"""
        child1 = ParentNode("li", [LeafNode(None, "Item 1")])
        child2 = ParentNode("li", [LeafNode(None, "Item 2")])
        child3 = ParentNode("li", [LeafNode(None, "Item 3")])
        
        parent = ParentNode("ul", [child1, child2, child3])
        expected = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        self.assertEqual(parent.to_html(), expected)
    
    def test_to_html_complex_nesting_with_props(self):
        """Test complex nesting with various props"""
        img = LeafNode("img", "", {"src": "pic.jpg", "alt": "Picture"})
        caption = LeafNode("p", "A beautiful picture")
        figure = ParentNode("figure", [img, caption], {"class": "image-container"})
        article = ParentNode("article", [figure], {"id": "main-article"})
        
        expected = ('<article id="main-article">'
                   '<figure class="image-container">'
                   '<img src="pic.jpg" alt="Picture"></img>'
                   '<p>A beautiful picture</p>'
                   '</figure>'
                   '</article>')
        self.assertEqual(article.to_html(), expected)
    
    def test_to_html_no_tag_raises_error(self):
        """Test that parent node with no tag raises ValueError"""
        child = LeafNode("span", "test")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no tag")
    
    def test_to_html_no_children_raises_error(self):
        """Test that parent node with no children raises ValueError"""
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no children")
    
    def test_to_html_empty_children_list(self):
        """Test parent node with empty children list"""
        parent = ParentNode("div", [])
        # Should work - empty list is valid, just produces empty content
        self.assertEqual(parent.to_html(), "<div></div>")
    
    def test_constructor_sets_value_to_none(self):
        """Test that ParentNode constructor sets value to None"""
        child = LeafNode("span", "test")
        parent = ParentNode("div", [child])
        self.assertIsNone(parent.value)
    
    def test_constructor_with_props(self):
        """Test constructor with props"""
        child = LeafNode("span", "test")
        props = {"class": "container", "id": "main"}
        parent = ParentNode("div", [child], props)
        self.assertEqual(parent.props, props)
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])
    
    def test_constructor_without_props(self):
        """Test constructor without props"""
        child = LeafNode("span", "test")
        parent = ParentNode("div", [child])
        self.assertIsNone(parent.props)
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child])


def run_tests():
    """Helper function to run tests when script is executed directly"""
    unittest.main()


if __name__ == "__main__":
    run_tests()
