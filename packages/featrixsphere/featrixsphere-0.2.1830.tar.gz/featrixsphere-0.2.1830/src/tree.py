from pathlib import Path

def build_tree(path: Path):
    tree = {}
    # order by creation date, from oldest to newest files
    items = sorted(Path(path).rglob('*'), key=lambda p: p.stat().st_ctime)
    for item in items:
        node = tree
        for part in item.relative_to(path).parts:
            node = node.setdefault(part, {})
    return {str(path): tree}



