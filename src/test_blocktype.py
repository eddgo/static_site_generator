import unittest
from blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        # Arrange
        block = "# Heading1"
        # Act
        expected_blocktype = BlockType.HEADING1
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "## Heading2"
        # Act
        expected_blocktype = BlockType.HEADING2
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "### Heading3"
        # Act
        expected_blocktype = BlockType.HEADING3
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "#### Heading4"
        # Act
        expected_blocktype = BlockType.HEADING4
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "##### Heading5"
        # Act
        expected_blocktype = BlockType.HEADING5
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "###### Heading6"
        # Act
        expected_blocktype = BlockType.HEADING6
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "```this is a code block \nwith more the one line\n and stuff```"
        # Act
        expected_blocktype = BlockType.CODE
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = ">This is a quote with\n>more then one line"
        # Act
        expected_blocktype = BlockType.QUOTE
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "- first entry\n- second entry\n- third entry"
        # Act
        expected_blocktype = BlockType.UNORDERED_LIST
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)

        # Arrange
        block = "1. first entry\n2. second entry\n3. third entry"
        # Act
        expected_blocktype = BlockType.ORDERED_LIST
        # Assert
        self.assertEqual(block_to_block_type(block), expected_blocktype)


if __name__ == '__main__':
    unittest.main()
