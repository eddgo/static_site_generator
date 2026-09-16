from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    HEADING4 = "heading4"
    HEADING5 = "heading5"
    HEADING6 = "heading6"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block) -> BlockType:
    lines = block.split("\n")

    if block.startswith("# "):
        return BlockType.HEADING1
    elif block.startswith("## "):
        return BlockType.HEADING2
    elif block.startswith("### "):
        return BlockType.HEADING3
    elif block.startswith("#### "):
        return BlockType.HEADING4
    elif block.startswith("##### "):
        return BlockType.HEADING5
    elif block.startswith("###### "):
        return BlockType.HEADING6
    elif block.startswith("```") and len(lines) > 1 and lines[-1].endswith("```"):
        return BlockType.CODE
    elif block.startswith(">") and len(lines) > 1 and lines[0].startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- ") and len(lines) > 1 and lines[-1].startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. ") and len(lines) > 1 and lines[-1].startswith(f"{len(lines)}. "):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH