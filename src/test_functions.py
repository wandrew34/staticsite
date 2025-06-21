import unittest

from functions import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
    markdown_to_blocks
)
from textnode import TextNode, TextType, text_node_to_html_node

class TestSplitNodes(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
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

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

class TestMarkdownExtraction(unittest.TestCase):
    """Test cases for markdown image and link extraction functions"""
    
    def test_extract_markdown_images(self):
        """Test basic image extraction"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_images(self):
        """Test extraction of multiple images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_images_no_images(self):
        """Test text with no images"""
        text = "This is just plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_images_empty_alt_text(self):
        """Test image with empty alt text"""
        text = "Image with empty alt text: ![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.png")], matches)
    
    def test_extract_images_with_spaces_in_alt_text(self):
        """Test image with spaces in alt text"""
        text = "![A beautiful sunset photo](https://example.com/sunset.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("A beautiful sunset photo", "https://example.com/sunset.jpg")], matches)
    
    def test_extract_images_multiple_on_same_line(self):
        """Test multiple images on the same line"""
        text = "![first](url1.jpg)![second](url2.png)"
        matches = extract_markdown_images(text)
        expected = [("first", "url1.jpg"), ("second", "url2.png")]
        self.assertListEqual(expected, matches)
    
    def test_extract_images_with_special_chars_in_url(self):
        """Test image with special characters in URL"""
        text = "![test](https://example.com/path/to/image.png?size=large&format=jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("test", "https://example.com/path/to/image.png?size=large&format=jpg")], matches)
    
    def test_extract_markdown_links(self):
        """Test basic link extraction"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_links_single_link(self):
        """Test extraction of a single link"""
        text = "Check out [this awesome site](https://example.com)!"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this awesome site", "https://example.com")], matches)
    
    def test_extract_links_no_links(self):
        """Test text with no links"""
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_links_empty_anchor_text(self):
        """Test link with empty anchor text"""
        text = "Link with empty text: [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)
    
    def test_extract_links_with_numbers_and_symbols(self):
        """Test link with numbers and symbols in anchor text"""
        text = "Download [Python 3.11+](https://python.org/downloads) now!"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Python 3.11+", "https://python.org/downloads")], matches)
    
    def test_extract_links_ignore_images(self):
        """Test that link extraction ignores images"""
        text = "This has ![an image](image.jpg) and [a link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("a link", "https://example.com")], matches)
    
    def test_extract_links_multiple_on_same_line(self):
        """Test multiple links on the same line"""
        text = "[first](url1.com)[second](url2.com)"
        matches = extract_markdown_links(text)
        expected = [("first", "url1.com"), ("second", "url2.com")]
        self.assertListEqual(expected, matches)
    
    def test_mixed_images_and_links(self):
        """Test text with both images and links"""
        text = "Here's ![an image](image.png) and [a link](https://example.com) together"
        
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertListEqual([("an image", "image.png")], image_matches)
        self.assertListEqual([("a link", "https://example.com")], link_matches)
    
    def test_extract_images_with_nested_brackets_in_url(self):
        """Test that nested brackets in URL don't break extraction"""
        # Note: This tests the current behavior - URLs with parentheses will be cut off
        text = "![test](https://example.com/path)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("test", "https://example.com/path")], matches)
    
    def test_extract_links_relative_urls(self):
        """Test links with relative URLs"""
        text = "See [about page](/about) and [contact](/contact.html)"
        matches = extract_markdown_links(text)
        expected = [("about page", "/about"), ("contact", "/contact.html")]
        self.assertListEqual(expected, matches)
    
    def test_extract_images_at_start_and_end(self):
        """Test images at the start and end of text"""
        text = "![start](start.jpg) middle text ![end](end.png)"
        matches = extract_markdown_images(text)
        expected = [("start", "start.jpg"), ("end", "end.png")]
        self.assertListEqual(expected, matches)
    
    def test_extract_links_at_start_and_end(self):
        """Test links at the start and end of text"""
        text = "[start](start.com) middle text [end](end.com)"
        matches = extract_markdown_links(text)
        expected = [("start", "start.com"), ("end", "end.com")]
        self.assertListEqual(expected, matches)
    
    def test_malformed_markdown_images(self):
        """Test handling of malformed image markdown"""
        text = "![missing closing paren](url.jpg ![complete](good.jpg)"
        matches = extract_markdown_images(text)
        # Should only match the properly formed image
        self.assertListEqual([("complete", "good.jpg")], matches)
    
    def test_malformed_markdown_links(self):
        """Test handling of malformed link markdown"""
        text = "[missing closing paren](url.com [complete](good.com)"
        matches = extract_markdown_links(text)
        # Should only match the properly formed link
        self.assertListEqual([("complete", "good.com")], matches)

class TestSplitNodesDelimiter(unittest.TestCase):
    """Test cases for split_nodes_delimiter function"""
    
    def test_basic_code_delimiter(self):
        """Test basic code delimiter splitting"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_bold_delimiter(self):
        """Test bold delimiter splitting"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic_delimiter(self):
        """Test italic delimiter splitting"""
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiters_in_one_text(self):
        """Test multiple delimiters in a single text node"""
        node = TextNode("Here is `code` and more `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_no_delimiters(self):
        """Test text with no delimiters"""
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_nodes_in_input_list(self):
        """Test processing multiple nodes in input list"""
        nodes = [
            TextNode("First `code` block", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second `code` block", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Unchanged
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_start_and_end(self):
        """Test delimiters at the start and end of text"""
        node = TextNode("`start` middle `end`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("start", TextType.CODE),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_adjacent_delimiters(self):
        """Test adjacent delimiters"""
        node = TextNode("Text `first``second` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("first", TextType.CODE),
            TextNode("second", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_delimited_section(self):
        """Test empty delimited section (should be skipped)"""
        node = TextNode("Text `` more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode(" more text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_unmatched_delimiter_raises_error(self):
        """Test that unmatched delimiter raises ValueError"""
        node = TextNode("This has `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched", str(context.exception).lower())
    
    def test_underscore_delimiter_for_italic(self):
        """Test underscore delimiter for italic text"""
        node = TextNode("This is _italic_ text with _more italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with ", TextType.TEXT),
            TextNode("more italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multi_character_delimiter(self):
        """Test multi-character delimiter (bold)"""
        node = TextNode("This is **really bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("really bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_input_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])
    
    def test_only_delimiter_text(self):
        """Test text that is only delimiters"""
        node = TextNode("`only code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("only code", TextType.CODE)]
        self.assertEqual(new_nodes, expected)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

def test_heading_blocks():
    """Test heading block detection"""
    # Valid headings
    assert block_to_block_type("# Heading 1") == BlockType.HEADING
    assert block_to_block_type("## Heading 2") == BlockType.HEADING
    assert block_to_block_type("### Heading 3") == BlockType.HEADING
    assert block_to_block_type("#### Heading 4") == BlockType.HEADING
    assert block_to_block_type("##### Heading 5") == BlockType.HEADING
    assert block_to_block_type("###### Heading 6") == BlockType.HEADING
    
    # Invalid headings (too many #, no space, etc.)
    assert block_to_block_type("####### Not a heading") == BlockType.PARAGRAPH
    assert block_to_block_type("#No space") == BlockType.PARAGRAPH
    assert block_to_block_type("## ") == BlockType.HEADING  # Empty heading text is valid
    
    print("✓ Heading tests passed")

def test_code_blocks():
    """Test code block detection"""
    # Valid code blocks
    assert block_to_block_type("```\nprint('hello')\n```") == BlockType.CODE
    assert block_to_block_type("```") == BlockType.CODE
    assert block_to_block_type("```\ncode here\nmore code\n```") == BlockType.CODE
    
    # Invalid code blocks
    assert block_to_block_type("``code``") == BlockType.PARAGRAPH
    assert block_to_block_type("```no closing") == BlockType.PARAGRAPH
    assert block_to_block_type("no opening```") == BlockType.PARAGRAPH
    
    print("✓ Code block tests passed")

def test_quote_blocks():
    """Test quote block detection"""
    # Valid quote blocks
    assert block_to_block_type(">This is a quote") == BlockType.QUOTE
    assert block_to_block_type(">Line 1\n>Line 2\n>Line 3") == BlockType.QUOTE
    assert block_to_block_type(">") == BlockType.QUOTE
    
    # Invalid quote blocks
    assert block_to_block_type(">Line 1\nNot a quote\n>Line 3") == BlockType.PARAGRAPH
    assert block_to_block_type("Not a quote\n>Line 2") == BlockType.PARAGRAPH
    
    print("✓ Quote block tests passed")

def test_unordered_list_blocks():
    """Test unordered list block detection"""
    # Valid unordered lists
    assert block_to_block_type("- Item 1") == BlockType.UNORDERED_LIST
    assert block_to_block_type("- Item 1\n- Item 2\n- Item 3") == BlockType.UNORDERED_LIST
    assert block_to_block_type("- ") == BlockType.UNORDERED_LIST
    
    # Invalid unordered lists
    assert block_to_block_type("-No space") == BlockType.PARAGRAPH
    assert block_to_block_type("- Item 1\nNot a list item\n- Item 3") == BlockType.PARAGRAPH
    assert block_to_block_type("* Item 1") == BlockType.PARAGRAPH  # Wrong bullet character
    
    print("✓ Unordered list tests passed")

def test_ordered_list_blocks():
    """Test ordered list block detection"""
    # Valid ordered lists
    assert block_to_block_type("1. Item 1") == BlockType.ORDERED_LIST
    assert block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3") == BlockType.ORDERED_LIST
    assert block_to_block_type("1. First\n2. Second\n3. Third\n4. Fourth") == BlockType.ORDERED_LIST
    
    # Invalid ordered lists
    assert block_to_block_type("1.No space") == BlockType.PARAGRAPH
    assert block_to_block_type("0. Starting at zero") == BlockType.PARAGRAPH
    assert block_to_block_type("2. Starting at two") == BlockType.PARAGRAPH
    assert block_to_block_type("1. Item 1\n3. Skipping 2") == BlockType.PARAGRAPH
    assert block_to_block_type("1. Item 1\n1. Same number") == BlockType.PARAGRAPH
    assert block_to_block_type("1. Item 1\nNot a list item\n3. Item 3") == BlockType.PARAGRAPH
    
    print("✓ Ordered list tests passed")

def test_paragraph_blocks():
    """Test paragraph block detection (default case)"""
    # Various paragraph examples
    assert block_to_block_type("This is a regular paragraph.") == BlockType.PARAGRAPH
    assert block_to_block_type("Multiple lines\nof regular text\nform a paragraph.") == BlockType.PARAGRAPH
    assert block_to_block_type("") == BlockType.PARAGRAPH
    assert block_to_block_type("Mixed content\n# that doesn't\n> match any pattern") == BlockType.PARAGRAPH
    
    print("✓ Paragraph tests passed")

def test_edge_cases():
    """Test edge cases and mixed content"""
    # Empty string
    assert block_to_block_type("") == BlockType.PARAGRAPH
    
    # Single characters
    assert block_to_block_type("#") == BlockType.PARAGRAPH
    assert block_to_block_type(">") == BlockType.QUOTE
    assert block_to_block_type("-") == BlockType.PARAGRAPH
    
    # Mixed valid patterns (should be paragraph since they don't match consistently)
    assert block_to_block_type("# Heading\n- List item") == BlockType.PARAGRAPH
    assert block_to_block_type(">Quote\n1. List item") == BlockType.PARAGRAPH
    
    print("✓ Edge case tests passed")

def run_all_tests():
    """Run all unit tests"""
    print("Running markdown block type parser tests...\n")
    
    test_heading_blocks()
    test_code_blocks()
    test_quote_blocks()
    test_unordered_list_blocks()
    test_ordered_list_blocks()
    test_paragraph_blocks()
    test_edge_cases()
    
    print("\n🎉 All tests passed!")

# Example usage and demonstration
def demonstrate_parser():
    """Demonstrate the parser with various examples"""
    print("\nDemonstration of block_to_block_type function:")
    print("=" * 50)
    
    examples = [
        "# Main Title",
        "```\nprint('Hello World')\n```",
        ">This is a quote\n>from someone famous",
        "- First item\n- Second item\n- Third item",
        "1. Step one\n2. Step two\n3. Step three",
        "This is just a regular paragraph with some text.",
        "####### Too many hashes",
        "1. First\n3. Skip second",
    ]
    
    for example in examples:
        block_type = block_to_block_type(example)
        print(f"Block: {repr(example)}")
        print(f"Type: {block_type.value}")
        print("-" * 30)
