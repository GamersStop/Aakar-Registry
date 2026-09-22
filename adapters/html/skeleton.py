import sys
from tree_sitter import Language, Parser
import tree_sitter_html as tshtml

HTML_LANGUAGE = Language(tshtml.language())
parser = Parser(HTML_LANGUAGE)

def prune_element(node, indent=0) -> str:
    spacing = "  " * indent
    if node.type == "element":
        start_tag_node = node.child_by_field_name("start_tag") or (node.children[0] if node.children else None)
        if not start_tag_node:
            return ""
        
        tag_text = start_tag_node.text.decode("utf-8").strip()
        tag_name = tag_text.split()[0].replace("<", "").replace(">", "").strip()
        
        # Collapse SVGs into single placeholder tag
        if tag_name.lower() == "svg":
            return f"{spacing}<svg ...><!-- icon omitted --></svg>\n"

        children_repr = []
        for child in node.children:
            if child.type == "element":
                children_repr.append(prune_element(child, indent + 1))
        
        if children_repr:
            return f"{spacing}{tag_text}\n{''.join(children_repr)}{spacing}</{tag_name}>\n"
        return f"{spacing}{tag_text}...<{tag_name}/>\n"
    
    return ""

def extract_skeleton(html_content: str) -> str:
    tree = parser.parse(bytes(html_content, "utf-8"))
    skeleton = []
    for child in tree.root_node.children:
        if child.type == "element":
            skeleton.append(prune_element(child))
    return "".join(skeleton)

if __name__ == "__main__":
    content = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    print(extract_skeleton(content))