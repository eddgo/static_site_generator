import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        # Arrange
        node = TextNode("This is text with a **bold text** in a normal text", TextType.TEXT)
        # Act
        actual_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(actual_nodes)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in a normal text", TextType.TEXT),
        ]
        # Assert
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_italic(self):
        # Arrange
        node = TextNode("This is text with a _italic text_ in a normal text", TextType.TEXT)
        # Act
        actual_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        print(actual_nodes)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" in a normal text", TextType.TEXT),
        ]
        # Assert
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_code(self):
        # Arrange
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        # Act
        actual_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        print(actual_nodes)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        # Assert
        self.assertEqual(actual_nodes, expected_nodes)

    def test_split_nodes_delimiter_italic_on_non_italic_textnode(self):
        # Arrange
        nodes = [
            TextNode("This is some text", TextType.TEXT),
            TextNode("This is **bold** text", TextType.TEXT),
        ]
        # Act
        actual_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        print(actual_nodes)
        expected_nodes = [
            TextNode("This is some text", TextType.TEXT),
            TextNode("This is **bold** text", TextType.TEXT),
        ]
        # Assert
        self.assertEqual(actual_nodes, expected_nodes)


if __name__ == '__main__':
    unittest.main()
