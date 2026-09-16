import re

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from blocktype import BlockType, block_to_block_type


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def text_to_textnodes(text) -> list[TextNode]:
    raw_text = text
    old_text_nodes = [TextNode(raw_text,TextType.TEXT)]
    final_nodes = []
    bold_words = split_nodes_delimiter(old_text_nodes, "**", TextType.BOLD)
    italic_words = split_nodes_delimiter(bold_words, "_", TextType.ITALIC)
    code_words = split_nodes_delimiter(italic_words, "`", TextType.CODE)
    images = split_nodes_image(code_words)
    links = split_nodes_link(images)
    final_nodes.extend(links)

    return final_nodes

def markdown_to_blocks(markdown) -> list[str]:
    splited_markdown = markdown.split("\n\n")

    return_blocks = []
    for block in splited_markdown:
        if block == "":
            continue
        block_strip = block.strip()
        return_blocks.append(block_strip)

    return return_blocks


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)

    for text_node in text_nodes:
        if text_node.text.startswith(">"):
            text_node.text.replace(">","")
        children.append(text_node_to_html_node(text_node))

    return children

def text_to_list_children(text):
    list_items = text.split("\n")
    list_item_nodes = []
    for item in list_items:
        if item.startswith("- "):
            item = item.replace("- ", "")
        cleaned_item = re.sub(r"(?<![^\s>])([0-9]+)\. ", "", item)
        text_nodes = text_to_textnodes(cleaned_item)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        li_node = ParentNode(tag="li", children=html_nodes)
        list_item_nodes.append(li_node)
    return list_item_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html = []
    for block in blocks:
       block_type = block_to_block_type(block)
       match block_type:
        case BlockType.HEADING1:
            block = block.replace("# ", "")
            html.append(ParentNode(tag = "h1", children=text_to_children(block)))
        case BlockType.HEADING2:
            block = block.replace("## ", "")
            html.append(ParentNode(tag = "h2", children=text_to_children(block)))
        case BlockType.HEADING3:
            block = block.replace("### ", "")
            html.append(ParentNode(tag = "h3", children=text_to_children(block)))
        case BlockType.HEADING4:
            block = block.replace("#### ", "")
            html.append(ParentNode(tag= "h4", children=text_to_children(block)))
        case BlockType.HEADING5:
            block = block.replace("##### ", "")
            html.append(ParentNode(tag= "h5", children=text_to_children(block)))
        case BlockType.HEADING6:
            block = block.replace("###### ", "")
            html.append(ParentNode(tag= "h6", children=text_to_children(block)))
        case BlockType.CODE:
                block_lines = block.split("\n")
                code_text = ""
                for block_line in block_lines:
                    if block_line.startswith("```"):
                        continue
                    elif block_line.endswith("```"):
                        continue
                    else:
                        code_text += block_line.strip() + "\n"

                pre_node = ParentNode(tag= "pre", children = [LeafNode(tag="code", value=code_text)])
                html.append(pre_node)
        case BlockType.QUOTE:
                block = block.replace(">","")
                block = block.strip()
                html.append(ParentNode(tag="blockquote", children=text_to_children(block)))
        case BlockType.UNORDERED_LIST:
                pre_node = ParentNode(tag="ul", children=text_to_list_children(block))
                html.append(pre_node)
        case BlockType.ORDERED_LIST:
                pre_node = ParentNode(tag="ol", children=text_to_list_children(block))
                html.append(pre_node)
        case BlockType.PARAGRAPH:
                block_text = block.replace("\n"," ")
                html.append(ParentNode(tag="p", children=text_to_children(block_text)))
    return ParentNode(tag="div", children = html)

def extract_title(markdown):
    title = ""
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line.startswith("# "):
            title = line[1:]
            title = title.strip()
    return title


