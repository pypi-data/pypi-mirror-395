import os
import fnmatch
from typing import List, Dict, Any

DirTree = Dict[str, Any]

def _build_tree(root_path: str, patterns: List[str]) -> DirTree:
    """Creates a nested dictionary representing the directory structure in the specified path."""
    tree: DirTree = {'files': [], 'dirs': {}}
    try:
        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            if os.path.isdir(item_path):
                subtree = _build_tree(item_path, patterns)
                if subtree['files'] or subtree['dirs']:
                    tree['dirs'][item] = subtree
            elif os.path.isfile(item_path):
                if any(fnmatch.fnmatch(item, pattern) for pattern in patterns):
                    tree['files'].append(item)
    except OSError as e:
        print(f"Warning: Could not access path {root_path}: {e}")
    return tree

def _write_tree_to_markdown(md_file, tree: DirTree, level: int):
    """Writes the tree data structure to the file in markdown format."""
    indent = '    ' * level
    for filename in sorted(tree['files']):
        md_file.write(f"{indent}- [] {filename}\n")
    
    for dirname, subtree in sorted(tree['dirs'].items()):
        md_file.write(f"{'    ' * (level -1)}{'#' * (level + 1)} {dirname}\n")
        _write_tree_to_markdown(md_file, subtree, level + 1)

def generate_global_markdown_listing(directories: List[str], file_patterns: List[str], output_file: str):
    """Creates a hierarchical list of markdown files for global directories. Uses the absolute path as the top heading and relative names for children."""
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for directory in directories:
            abs_dir = os.path.abspath(directory)
            
            if not os.path.isdir(abs_dir):
                print(f"Warning: Global directory not found: {abs_dir}")
                md_file.write(f"# {directory}\n")
                md_file.write(f"    - !! Warning: Global directory not found: {abs_dir}\n\n")
                continue

            tree = _build_tree(abs_dir, file_patterns)

            if tree['files'] or tree['dirs']:
                md_file.write(f"# {abs_dir}\n")
                _write_tree_to_markdown(md_file, tree, 1)
                md_file.write("\n")